-- Insert Suppliers (omit Supplier_ID)
INSERT INTO Supplier (Supplier_Name, Contact_Name, Contact_Email, Contact_Phone)
VALUES
  ('Beautisa', 'Laura Pierre', 'laura.p@beautisa.com', '919-991-1199'),
  ('Beats by Dre', 'John Smith', 'johnsmith@beatsbydre.com', '209-902-2200');

-- Insert Products (omit Product_ID)
INSERT INTO [Product] (Product_Name, Product_Description, Category_ID, Supplier_ID)
VALUES
  ('Hair Spray Bottle', 'Ultra fine mist water sprayer for hairstyling and cleaning 2 pack 6.8 oz', 1, 1),
  ('Beats Powerbeats Pro 2', 'Wireless bluetooth earbuds - noise cancelling', 2, 2);

-- Insert Purchase Orders (omit Purchase_Order_ID)
INSERT INTO Purchase_Order (Supplier_ID, Order_Date, Purchase_Order_Status)
VALUES
  (1, "2025-04-11", 'Received'),
  (2, "2025-04-13", 'Pending'),
  (1, "2025-04-15", 'Pending');

-- Insert Purchase Order Items (omit Purchase_Order_Item_ID)
INSERT INTO Purchase_Order_Item (Purchase_Order_ID, Product_ID, Quantity)
VALUES
  (1, 1, 500),
  (2, 1, 250),
  (3, 2, 75);

-- Insert Inventory records (omit Inventory_ID)
INSERT INTO Inventory (Product_ID, Quantity, Unit_Price)
VALUES
  (1, 3000, 6.99),
  (2, 100, 249.00);
