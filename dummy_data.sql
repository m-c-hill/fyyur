INSERT INTO venue (name, city, state, address, phone, image_link, genres, facebook_link, website_link, seeking_talent, seeking_description, date_listed)
VALUES
('The Musical Hop', 'San Francisco','CA', '1015 Folsom Street', '123-123-1234', 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', ARRAY ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'], 'https://www.facebook.com/TheMusicalHop', 'https://www.themusicalhop.com', True, 'We are on the lookout for a local artist to play every two weeks. Please call us.', '2021-07-29T21:30:00.000Z'),
('The Dueling Pianos Bar', 'New York', 'NY', '335 Delancey Street', '914-003-1132', 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', ARRAY ['Classical', 'R&B', 'Hip-Hop'], 'https://www.facebook.com/theduelingpianos', 'https://www.theduelingpianos.com', False, Null, '2021-07-29T21:30:00.000Z'),
('Park Square Live Music & Coffee', 'San Francisco', 'CA', '34 Whiskey Moore Ave', '415-000-1234', 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', ARRAY ['Rock n Roll', 'Jazz', 'Classical', 'Folk'], 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', 'https://www.parksquarelivemusicandcoffee.com', False, Null, '2022-07-29T21:30:00.000Z');


INSERT INTO artist (name, genres, city, state, phone, facebook_link, website_link, seeking_venue, seeking_description, image_link, date_listed)
VALUES
('Guns N Petals', ARRAY ['Rock n Roll'], 'San Francisco', 'CA', '326-123-5000', 'https://www.facebook.com/GunsNPetals', 'https://www.gunsnpetalsband.com', True, 'Looking for shows to perform at in the San Francisco Bay Area!', 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80', '2019-07-21T21:30:00.000Z'),
('Matt Quevedo', ARRAY ['Jazz'], 'New York', 'NY', '300-400-5000', 'https://www.facebook.com/mattquevedo923251523', Null, False, Null, 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', '2019-07-21T21:30:00.000Z'),
('The Wild Sax Band', ARRAY ['Jazz', 'Classical'], 'San Francisco', 'CA', '432-325-5432', Null, Null, False, Null, 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80', '2022-07-29T21:30:00.000Z');


INSERT INTO show (artist_id, venue_id, start_time, date_listed)
VALUES
(1, 1, '2020-05-21T21:30:00.000Z', '2019-07-21T21:30:00.000Z'),
(2, 3, '2020-06-15T23:00:00.000Z', '2019-07-21T21:30:00.000Z'),
(3, 3, '2035-04-01T20:00:00.000Z', '2022-07-29T21:30:00.000Z'),
(3, 3, '2035-04-08T20:00:00.000Z', '2022-07-29T21:30:00.000Z'),
(3, 3, '2035-04-15T20:00:00.000Z', '2022-07-29T21:30:00.000Z');
