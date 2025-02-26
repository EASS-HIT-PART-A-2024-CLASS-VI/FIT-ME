--
-- PostgreSQL database dump
--

-- Dumped from database version 13.18 (Debian 13.18-1.pgdg120+1)
-- Dumped by pg_dump version 13.18 (Debian 13.18-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.clients (
    phone_number character varying NOT NULL,
    id_number character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    membership_type character varying NOT NULL,
    payment_method character varying NOT NULL,
    date_of_birth date
);


ALTER TABLE public.clients OWNER TO gym_admin;

--
-- Name: group_lessons; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.group_lessons (
    day character varying NOT NULL,
    "time" character varying NOT NULL,
    class_name character varying NOT NULL,
    instructor_name character varying NOT NULL
);


ALTER TABLE public.group_lessons OWNER TO gym_admin;

--
-- Name: gym_staff; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.gym_staff (
    id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    role character varying NOT NULL,
    phone_number character varying NOT NULL,
    date_of_birth date NOT NULL
);


ALTER TABLE public.gym_staff OWNER TO gym_admin;

--
-- Name: gym_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: gym_admin
--

CREATE SEQUENCE public.gym_staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gym_staff_id_seq OWNER TO gym_admin;

--
-- Name: gym_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gym_admin
--

ALTER SEQUENCE public.gym_staff_id_seq OWNED BY public.gym_staff.id;


--
-- Name: interested_clients; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.interested_clients (
    phone_number character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL
);


ALTER TABLE public.interested_clients OWNER TO gym_admin;

--
-- Name: past_clients; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.past_clients (
    phone_number character varying NOT NULL,
    id_number character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    date_of_birth date,
    membership_type character varying NOT NULL,
    payment_method character varying NOT NULL
);


ALTER TABLE public.past_clients OWNER TO gym_admin;

--
-- Name: personal_trainings; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.personal_trainings (
    day character varying NOT NULL,
    "time" character varying NOT NULL,
    trainee_name character varying NOT NULL,
    trainer_name character varying NOT NULL
);


ALTER TABLE public.personal_trainings OWNER TO gym_admin;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.tasks (
    phone_number character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    description character varying
);


ALTER TABLE public.tasks OWNER TO gym_admin;

--
-- Name: users; Type: TABLE; Schema: public; Owner: gym_admin
--

CREATE TABLE public.users (
    username character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.users OWNER TO gym_admin;

--
-- Name: gym_staff id; Type: DEFAULT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.gym_staff ALTER COLUMN id SET DEFAULT nextval('public.gym_staff_id_seq'::regclass);


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.clients (phone_number, id_number, first_name, last_name, membership_type, payment_method, date_of_birth) FROM stdin;
1234567890	987654321	John	Doe	monthly	credit card	1990-01-01
0587040145	455878987	Sagi	Levi	monthly	cash	1978-02-28
0581010123	122336547	Riki	Sharon	yearly	cash	2025-02-26
0587898898	855214569	Riki	Sharon	yearly	cash	1994-02-28
0587878787	255858965	Shirly	Jan	yearly	cash	1994-04-12
0588050258	255451236	Sharon	Levin	quarterly	credit card	1995-02-28
0521020304	123456789	Liat	Saron	yearly	credit card	1992-02-27
\.


--
-- Data for Name: group_lessons; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

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


--
-- Data for Name: gym_staff; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.gym_staff (id, first_name, last_name, role, phone_number, date_of_birth) FROM stdin;
2	Sarit	Hadad	Manager	0564738298	1992-02-28
3	Daniel	Hadad	Trainer	0567676567	1992-02-12
4	Adir	Gelkop	Trainer	0588080852	1997-02-27
5	Liat	Simhayev	Trainer	0587010123	1997-05-15
6	Or	Dorbin	Trainer	0589999987	1993-02-28
7	Or	Segal	Receptionist	0587898658	1993-03-10
8	Shilat	Mari	Receptionist	0587040458	1987-03-26
\.


--
-- Data for Name: interested_clients; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.interested_clients (phone_number, first_name, last_name) FROM stdin;
0584080256	Shir	Bitan
0532121324	Teddi	Dan
0587070745	Jessica	Jully
0541010147	Rita	Levin
\.


--
-- Data for Name: past_clients; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.past_clients (phone_number, id_number, first_name, last_name, date_of_birth, membership_type, payment_method) FROM stdin;
0584080658	588784589	Or	Dorbin	1997-02-27	monthly	credit card
0542314234	211453672	Shiri	Maimon	1995-02-28	yearly	credit card
0543628376	211348888	Sari	Hun	2001-05-23	quarterly	credit card
0589080789	777778787	Sharon	Gal	1994-03-15	yearly	credit card
0527020327	211487895	Liat	Simha	1999-02-25	quarterly	credit card
0528080987	123456788	Larisa	Cohen	1988-02-29	yearly	credit card
\.


--
-- Data for Name: personal_trainings; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

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


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.tasks (phone_number, first_name, last_name, description) FROM stdin;
0587070808	Shay	Chen	please call her afternoon :)
0587070745	Jessica	Jully	Jessica is interested in a gym membership. Please contact her/him ASAP.
0541010147	Rita	Levin	Rita is interested in a gym membership. Please contact her/him ASAP.
0588080805	Shiri	Maimon	please call her afternoon :) 
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: gym_admin
--

COPY public.users (username, password) FROM stdin;
ordo	Aa123456
Liatsim	Aa123456
Shoshi	Aa123456
sapirha	Aa123456
miriya	Aa123456
viciy	Aa123456
\.


--
-- Name: gym_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gym_admin
--

SELECT pg_catalog.setval('public.gym_staff_id_seq', 9, true);


--
-- Name: clients client_pk; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT client_pk PRIMARY KEY (phone_number, id_number);


--
-- Name: group_lessons group_lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.group_lessons
    ADD CONSTRAINT group_lessons_pkey PRIMARY KEY (day, "time");


--
-- Name: gym_staff gym_staff_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.gym_staff
    ADD CONSTRAINT gym_staff_phone_number_key UNIQUE (phone_number);


--
-- Name: gym_staff gym_staff_pkey; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.gym_staff
    ADD CONSTRAINT gym_staff_pkey PRIMARY KEY (id);


--
-- Name: interested_clients interested_clients_pkey; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.interested_clients
    ADD CONSTRAINT interested_clients_pkey PRIMARY KEY (phone_number);


--
-- Name: past_clients past_clients_pk; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.past_clients
    ADD CONSTRAINT past_clients_pk PRIMARY KEY (phone_number, id_number);


--
-- Name: personal_trainings personal_training_pk; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.personal_trainings
    ADD CONSTRAINT personal_training_pk PRIMARY KEY (trainer_name, day, "time");


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (phone_number);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: gym_admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- Name: ix_interested_clients_phone_number; Type: INDEX; Schema: public; Owner: gym_admin
--

CREATE INDEX ix_interested_clients_phone_number ON public.interested_clients USING btree (phone_number);


--
-- Name: ix_tasks_phone_number; Type: INDEX; Schema: public; Owner: gym_admin
--

CREATE INDEX ix_tasks_phone_number ON public.tasks USING btree (phone_number);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: gym_admin
--

CREATE INDEX ix_users_username ON public.users USING btree (username);


--
-- PostgreSQL database dump complete
--

