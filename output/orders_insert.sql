INSERT INTO orders (id, event_id, created, completed, price, address1, address2, country_code) VALUES ('10b2de12-2507-4df5-8559-7f05bbe64235', '31542e20-eb0d-4e8a-9071-25682909db67', '2024-02-05 14:49:15+0000', '2024-02-05 14:49:15+0000', 41996, '123 main st', 'shek kip mei, kowloon', 'HK') ON DUPLICATE KEY UPDATE id = VALUES(id), event_id = VALUES(event_id), created = VALUES(created), completed = VALUES(completed), price = VALUES(price), address1 = VALUES(address1), address2 = VALUES(address2), country_code = VALUES(country_code);
INSERT INTO orders (id, event_id, created, completed, price, address1, address2, country_code) VALUES ('b70f04ca-70ae-45ea-aced-ba8b7d71988a', 'fe36e60a-384d-4785-a9f6-6b6464bdd023', '2024-02-05 14:49:15+0000', '2024-02-05 14:49:15+0000', 16990, '40 boundary rd', 'tsim sha tsui, kowloon', 'HK') ON DUPLICATE KEY UPDATE id = VALUES(id), event_id = VALUES(event_id), created = VALUES(created), completed = VALUES(completed), price = VALUES(price), address1 = VALUES(address1), address2 = VALUES(address2), country_code = VALUES(country_code);
INSERT INTO orders (id, event_id, created, completed, price, address1, address2, country_code) VALUES ('51b1d3b4-da4a-434d-872f-6948c1926f13', 'fe36e60a-384d-4785-a9f6-6b6464bdd023', '2024-02-05 14:49:15+0000', '2024-02-05 14:49:15+0000', 16990, '1288 Lianhua Road', 'Futian District, Shenzhen, Guangdong', 'CN') ON DUPLICATE KEY UPDATE id = VALUES(id), event_id = VALUES(event_id), created = VALUES(created), completed = VALUES(completed), price = VALUES(price), address1 = VALUES(address1), address2 = VALUES(address2), country_code = VALUES(country_code);
INSERT INTO orders (id, event_id, created, completed, price, address1, address2, country_code) VALUES ('1f8e08ba-d013-428c-9926-b3b9e3e0debe', '288b6e25-e4ef-4e71-8138-c889deac9a91', '2024-02-05 14:49:15+0000', '2024-02-05 14:49:15+0000', 9000, '42 Rua de Madrid', 'Sé', 'MO') ON DUPLICATE KEY UPDATE id = VALUES(id), event_id = VALUES(event_id), created = VALUES(created), completed = VALUES(completed), price = VALUES(price), address1 = VALUES(address1), address2 = VALUES(address2), country_code = VALUES(country_code);
INSERT INTO orders (id, event_id, created, completed, price, address1, address2, country_code) VALUES ('07d41ce4-296e-4125-8a5d-0f2f5b60a212', '31542e20-eb0d-4e8a-9071-25682909db67', '2024-02-05 14:49:15+0000', '2024-02-05 14:49:15+0000', 11499, '1505 Avenida de Amizade', 'Taipa', 'MO') ON DUPLICATE KEY UPDATE id = VALUES(id), event_id = VALUES(event_id), created = VALUES(created), completed = VALUES(completed), price = VALUES(price), address1 = VALUES(address1), address2 = VALUES(address2), country_code = VALUES(country_code);
