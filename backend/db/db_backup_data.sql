-- PostgreSQL Data-Only Dump

--  clients
COPY public.clients (phone_number, id_number, first_name, last_name, membership_type, payment_method, date_of_birth) FROM stdin;
1234567890	987654321	John	Doe	monthly	credit card	1990-01-01
0587040145	455878987	Sagi	Levi	monthly	cash	1978-02-28
0581010123	122336547	Riki	Sharon	yearly	cash	2025-02-26
0587898898	855214569	Riki	Sharon	yearly	cash	1994-02-28
0587878787	255858965	Shirly	Jan	yearly	cash	1994-04-12
0588050258	255451236	Sharon	Levin	quarterly	credit card	1995-02-28
0521020304	123456789	Liat	Saron	yearly	credit card	1992-02-27
\.

-- group_lessons
COPY public.group_lessons (day, "time", class_name, instructor_name) FROM stdin;
Monday	08:00-09:00	Yoga	Alice
wednesday	12:00-12:55	Pilatis	Liat Simhaev
tuesday	12:00-12:55	Pilatis	Liat Simhaev
saturday	12:00-12:55	Pilatis	Liat Simhaev
sunday	12:00-12:55	Yoga	Liat Simhaev
thursday	11:00-11:55	Functional	Offer Nissim
wednesday	11:00-11:55	Functional	Offer Nissim
sunday	08:00-08:55	Yogilatis	Tal Levi
tuesday	10:00-10:55	Yogilatis	Tal Levi
sunday	10:00-10:55	Yoga	Liat Simhayev
tuesday	11:00-11:55	Yoga	Liat Simhayev
\.

-- gym_staff
COPY public.gym_staff (id, first_name, last_name, role, phone_number, date_of_birth) FROM stdin;
2	Sarit	Hadad	Manager	0564738298	1992-02-28
3	Daniel	Hadad	Trainer	0567676567	1992-02-12
4	Adir	Gelkop	Trainer	0588080852	1997-02-27
5	Liat	Simhayev	Trainer	0587010123	1997-05-15
6	Or	Dorbin	Trainer	0589999987	1993-02-28
7	Or	Segal	Receptionist	0587898658	1993-03-10
8	Shilat	Mari	Receptionist	0587040458	1987-03-26
\.

-- interested_clients
COPY public.interested_clients (phone_number, first_name, last_name) FROM stdin;
0584080256	Shir	Bitan
0532121324	Teddi	Dan
0587070745	Jessica	Jully
0541010147	Rita	Levin
\.

-- past_clients
COPY public.past_clients (phone_number, id_number, first_name, last_name, date_of_birth, membership_type, payment_method) FROM stdin;
0584080658	588784589	Or	Dorbin	1997-02-27	monthly	credit card
0542314234	211453672	Shiri	Maimon	1995-02-28	yearly	credit card
0543628376	211348888	Sari	Hun	2001-05-23	quarterly	credit card
0589080789	777778787	Sharon	Gal	1994-03-15	yearly	credit card
0527020327	211487895	Liat	Simha	1999-02-25	quarterly	credit card
0528080987	123456788	Larisa	Cohen	1988-02-29	yearly	credit card
\.

-- personal_trainings
COPY public.personal_trainings (day, "time", trainee_name, trainer_name) FROM stdin;
tuesday	10:00-10:55	Kelly shir	Or Dorbin
thursday	10:00-10:55	Kelly shir	Or Dorbin
sunday	10:00-10:55	Kelly shir	Or Dorbin
monday	10:00-10:55	Osher Cohen	Or Dorbin
friday	10:00-10:55	Osher Cohen	Or Dorbin
sunday	09:00-09:55	Sarit Hadad	Liat Simhayev
monday	13:00-13:55	Avital Bitan	Adir Gelkop
thursday	13:00-13:55	Avital Bitan	Adir Gelkop
wednesday	10:00-10:55	Sagi Levin	Adir Gelkop
monday	11:00-11:55	Omer Adam	Ori Levi
\.

-- tasks
COPY public.tasks (phone_number, first_name, last_name, description) FROM stdin;
0587070808	Shay	Chen	please call her afternoon :)
0587070745	Jessica	Jully	Jessica is interested in a gym membership. Please contact her/him ASAP.
0541010147	Rita	Levin	Rita is interested in a gym membership. Please contact her/him ASAP.
0588080805	Shiri	Maimon	please call her afternoon :) 
\.


