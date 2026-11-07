// Creates the "orders" collection with schema validation and indexes.
// Per D-013 (MongoDB collection for orders). Run with: mongosh <uri> mongo/001_create_orders_collection.js
// D-004: all timestamps are BSON Date, which MongoDB stores as UTC.

db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["customerId", "status", "totalCents", "currency", "createdAt", "updatedAt"],
      additionalProperties: true,
      properties: {
        customerId: { bsonType: ["objectId", "string", "long", "int"], description: "Customer reference" },
        status: {
          enum: ["pending", "paid", "shipped", "delivered", "cancelled"],
          description: "Order lifecycle state"
        },
        totalCents: { bsonType: ["long", "int"], minimum: 0, description: "Order total in minor units" },
        currency: { bsonType: "string", pattern: "^[A-Z]{3}$", description: "ISO 4217 code" },
        items: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["sku", "quantity", "unitPriceCents"],
            properties: {
              sku: { bsonType: "string" },
              quantity: { bsonType: ["int", "long"], minimum: 1 },
              unitPriceCents: { bsonType: ["int", "long"], minimum: 0 }
            }
          }
        },
        createdAt: { bsonType: "date", description: "UTC" },
        updatedAt: { bsonType: "date", description: "UTC" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

db.orders.createIndex({ customerId: 1 }, { name: "orders_customer_id_idx" });
db.orders.createIndex({ status: 1 }, { name: "orders_status_idx" });
db.orders.createIndex({ createdAt: -1 }, { name: "orders_created_at_idx" });

// Undo: db.orders.drop();
