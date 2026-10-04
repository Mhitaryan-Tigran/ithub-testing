import assert from "node:assert/strict";
import { after, before, test } from "node:test";
import { freshDb, queries } from "./db.mjs";

let db;
const q = queries();
const run = async (name) => (await db.query(q[name])).rows;

before(async () => { db = await freshDb(); });
after(async () => { await db.close(); });

test("1. клиенты с заказами в текущем месяце, по убыванию суммы", async () => {
  const rows = await run("customers_this_month");
  assert.deepEqual(rows.map((r) => [r.full_name, Number(r.total)]), [["Борис Егоров", 95000], ["Анна Волкова", 13900]]);
});

test("2. товары дороже средней цены своей категории, по возрастанию цены", async () => {
  const rows = await run("products_above_category_avg");
  assert.deepEqual(rows.map((r) => r.name), ["SQL для чайников", "Худи", "Смартфон", "Ноутбук"]);
  assert.ok(!rows.some((r) => r.name === "Чистый код"), "цена ровно равна средней по категории — строго больше не выполняется");
  for (let i = 1; i < rows.length; i++) assert.ok(Number(rows[i - 1].price) <= Number(rows[i].price));
});

test("3. заказы с электроникой, по дате", async () => {
  const rows = await run("electronics_orders");
  assert.deepEqual(rows.map((r) => r.id), [4, 1, 2]);
});

test("4. клиенты без заказов в прошлом году, по алфавиту", async () => {
  const rows = await run("customers_without_orders_last_year");
  assert.deepEqual(rows.map((r) => r.full_name), ["Анна Волкова", "Глеб Иванов", "Дарья Ким"]);
});

test("5. товары, которые ни разу не заказывали, по названию", async () => {
  const rows = await run("never_ordered_products");
  assert.deepEqual(rows.map((r) => r.name), ["Кабель USB-C", "Носки"]);
});

test("целостность: нельзя заказать несуществующий товар", async () => {
  await assert.rejects(db.query("INSERT INTO order_items VALUES (1, 999, 1, 10)"), /foreign key/);
});

test("целостность: цена и количество не могут быть отрицательными", async () => {
  await assert.rejects(db.query("INSERT INTO products (name, category_id, price) VALUES ('X', 1, -1)"), /check constraint/);
  await assert.rejects(db.query("INSERT INTO order_items VALUES (2, 3, 0, 10)"), /check constraint/);
});
