import redis from 'redis';
import express from 'express';
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = redis.createClient();
const hgetAsync = promisify(client.hget).bind(client);

const listProducts = [
  { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find(product => product.id === id);
};

app.get('/list_products', (req, res) => {
  const response = listProducts.map(({ id, name, price, stock }) => ({
    itemId: id,
    itemName: name,
    price,
    initialAvailableQuantity: stock,
  }));
  res.json(response);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: "Product not found" });
  };

  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity,
  });
});

function reserveStockById(itemId, stock) {
  client.hset(`item:${itemId}`, 'reserved', stock);
};

async function getCurrentReservedStockById(itemId) {
  const reserved = await hgetAsync(`item:${itemId}`, 'reserved');
  return reserved ? parseInt(reserved, 10) : 0;
};

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: "Product not found" });
  };

  const currentQuantity = await getCurrentReservedStockById(itemId);

  if (currentQuantity >= product.stock) {
  return res.json({
    status: "Not enough stock available",
    itemId: product.id,
  });
  };

  reserveStockById(itemId, currentQuantity + 1);
  res.json({
    status: "Reservation confirmed",
    itemId: product.id,
  });
});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
