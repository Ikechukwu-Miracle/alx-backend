const express = require('express');
const { promisify } = require('util');
const redis = require('redis');

const app = express();
const port = 1245;

// Data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Data access
function getItemById(id) {
  return listProducts.find(product => product.itemId === id);
}

// Server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

// Products route
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity
  })));
});

// Redis client
const client = redis.createClient();

client.on('connect', () => {
  console.log('Connected to Redis');
});

client.on('error', (err) => {
  console.error(`Redis error: ${err}`);
});

const reserveStockById = promisify(client.set).bind(client);
const getCurrentReservedStockById = promisify(client.get).bind(client);

// Product detail route
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(`item.${itemId}`);
  res.json({
    itemId: item.itemId,
    itemName: item.itemName,
    price: item.price,
    initialAvailableQuantity: item.initialAvailableQuantity,
    currentQuantity: parseInt(currentQuantity) || 0
  });
});

// Reserve product route
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(`item.${itemId}`);
  const availableQuantity = item.initialAvailableQuantity - (parseInt(currentQuantity) || 0);
  if (availableQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId: item.itemId });
  }

  await reserveStockById(`item.${itemId}`, 1);
  res.json({ status: 'Reservation confirmed', itemId: item.itemId });
});

module.exports = app; // Export app for testing purposes
