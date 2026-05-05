// 1. Switch to the database
use fastapi_nosql_db;

// 2. Insert Multiple Documents
db.products.insertMany([
  {
    name: "Mechanical Keyboard",
    description: "High-performance mechanical keyboard with RGB lighting",
    price: 120.50,
    category: "Electronics",
    seller_id: "user_001",
    reviews: [{ user: "bob", rating: 5, comment: "Great switches!" }]
  },
  {
    name: "Ergonomic Chair",
    description: "Premium ergonomic office chair with lumbar support",
    price: 350.00,
    category: "Furniture",
    seller_id: "user_002",
    reviews: []
  }
]);

// 3. Find with Query Operators ($gt = greater than, $eq = equals)
db.products.find({ price: { $gt: 150 } });

// 4. Projection (Return only the name and price, hide _id)
db.products.find({ category: "Electronics" }, { name: 1, price: 1, _id: 0 });

// 5. Update a Document (Add a review using $push)
db.products.updateOne(
  { name: "Ergonomic Chair" },
  { $push: { reviews: { user: "alice", rating: 4, comment: "Very comfortable." } } }
);

// 6. Aggregation Pipeline (Group by category and find average price)
db.products.aggregate([
  { $group: { _id: "$category", avgPrice: { $avg: "$price" }, totalItems: { $sum: 1 } } }
]);