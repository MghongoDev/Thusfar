// Creates the "orders" collection with schema validation and indexes.
// Run with: mongosh "<connection-string>/<db>" create_orders_collection.js
// Decisions: D-017 (MongoDB collection for orders), D-004 (all dates stored in UTC).
// All timestamps are BSON Date values, which MongoDB stores as UTC.

db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["orderNumber", "customerId", "status", "items", "total", "currency", "createdAt", "updatedAt"],
      additionalProperties: true,
      properties: {
        orderNumber: { bsonType: "string", description: "Unique human-facing order number" },
        customerId:  { bsonType: ["objectId", "string"], description: "Reference to the customer" },
        status: {
          enum: ["pending", "paid", "shipped", "delivered", "cancelled", "refunded"],
          description: "Order lifecycle state"
        },
        items: {
          bsonType: "array",
          minItems: 1,
          items: {
            bsonType: "object",
            required: ["sku", "name", "quantity", "unitPrice"],
            properties: {
              sku:       { bsonType: "string" },
              name:      { bsonType: "string" },
              quantity:  { bsonType: "int", minimum: 1 },
              unitPrice: { bsonType: "decimal", description: "Price per unit; Decimal128 avoids float rounding" }
            }
          }
        },
        total:    { bsonType: "decimal", description: "Order total; Decimal128" },
        currency: { bsonType: "string", pattern: "^[A-Z]{3}$", description: "ISO 4217 code" },
        shippingAddress: {
          bsonType: "object",
          properties: {
            line1:      { bsonType: "string" },
            line2:      { bsonType: "string" },
            city:       { bsonType: "string" },
            region:     { bsonType: "string" },
            postalCode: { bsonType: "string" },
            country:    { bsonType: "string", pattern: "^[A-Z]{2}$" }
          }
        },
        createdAt: { bsonType: "date", description: "UTC (D-004)" },
        updatedAt: { bsonType: "date", description: "UTC (D-004)" },
        paidAt:    { bsonType: ["date", "null"], description: "UTC (D-004)" },
        shippedAt: { bsonType: ["date", "null"], description: "UTC (D-004)" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

db.orders.createIndex({ orderNumber: 1 }, { unique: true, name: "uniq_orderNumber" });
db.orders.createIndex({ customerId: 1, createdAt: -1 }, { name: "customer_recent" });
db.orders.createIndex({ status: 1, createdAt: -1 }, { name: "status_recent" });
