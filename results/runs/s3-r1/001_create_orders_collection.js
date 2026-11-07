// Migration 001 (MongoDB): create the orders collection.
// D-005: MongoDB collection for orders (supersedes D-001).
// D-003: MongoDB was signed off by the override; this is a plain mongosh
//        script, so no migration library or other package is added.
// D-004: created_at / updated_at are BSON dates, which are always UTC.
//
// Run: mongosh "<connection-string>/<db>" mongo/001_create_orders_collection.js

db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["customer_id", "status", "total_cents", "currency", "created_at", "updated_at"],
      properties: {
        customer_id: { bsonType: "long", description: "customer id" },
        status: {
          enum: ["pending", "paid", "shipped", "delivered", "cancelled"],
          description: "order status"
        },
        total_cents: { bsonType: "long", minimum: 0, description: "total in minor units" },
        currency: { bsonType: "string", minLength: 3, maxLength: 3, description: "ISO 4217 code" },
        created_at: { bsonType: "date", description: "UTC (D-004)" },
        updated_at: { bsonType: "date", description: "UTC (D-004)" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

db.orders.createIndex({ customer_id: 1 }, { name: "orders_customer_id_idx" });
db.orders.createIndex({ status: 1, created_at: 1 }, { name: "orders_status_created_at_idx" });

// Down:
// db.orders.drop();
