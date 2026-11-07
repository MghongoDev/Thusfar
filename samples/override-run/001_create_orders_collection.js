// 001_create_orders_collection.js
// Creates the MongoDB "orders" collection (D-005, which supersedes D-001).
// Run with mongosh:  mongosh "<connection-uri>" 001_create_orders_collection.js
// All dates are BSON Date values, which MongoDB stores as UTC (D-004).
// Write them with new Date() or ISO strings ending in "Z"; never local-time strings.

db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["customer_id", "status", "total_cents", "currency", "placed_at", "created_at", "updated_at"],
      properties: {
        customer_id: { bsonType: "long", description: "customer id" },
        status: {
          enum: ["pending", "paid", "shipped", "cancelled", "refunded"],
          description: "order status"
        },
        total_cents: { bsonType: "long", minimum: 0, description: "order total in cents" },
        currency: { bsonType: "string", minLength: 3, maxLength: 3, description: "ISO 4217 code" },
        placed_at:  { bsonType: "date", description: "UTC (D-004)" },
        created_at: { bsonType: "date", description: "UTC (D-004)" },
        updated_at: { bsonType: "date", description: "UTC (D-004)" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

db.orders.createIndex({ customer_id: 1 }, { name: "orders_customer_id_idx" });
db.orders.createIndex({ status: 1, placed_at: 1 }, { name: "orders_status_placed_at_idx" });

// Down:
// db.orders.drop();
