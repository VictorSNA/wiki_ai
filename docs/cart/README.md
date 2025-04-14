# POST /api/v1/cart/add

Adds a product to the user’s shopping cart. If the product already exists in the cart, the quantity will be updated.

---

## Request Headers

| Key            | Value              | Required |
|----------------|--------------------|----------|
| Authorization  | Bearer `token`     | ✅        |
| Content-Type   | application/json   | ✅        |

---

## Request Body

```json
{
  "product_id": "abc123",
  "quantity": 2
}
```

| Field       | Type     | Description                                 | Required |
|-------------|----------|---------------------------------------------|----------|
| product_id  | string   | Unique identifier of the product            | ✅        |
| quantity    | integer  | Number of units to add to the shopping cart | ✅        |

---

## Response (200 OK)

```json
{
  "message": "Product added to cart successfully.",
  "cart_item": {
    "product_id": "abc123",
    "name": "Organic Bananas",
    "quantity": 2,
    "price_per_unit": 1.50,
    "total_price": 3.00
  }
}
```

---

## Response (400 Bad Request)

```json
{
  "error": "Invalid product ID or quantity."
}
```

---

## Response (401 Unauthorized)

```json
{
  "error": "Missing or invalid authorization token."
}
```

---

## Notes

- The `product_id` must exist in the product catalog.
- `quantity` must be greater than 0.
- Users must be authenticated to use this endpoint.
- If the product is already in the cart, its quantity will be incremented accordingly.
