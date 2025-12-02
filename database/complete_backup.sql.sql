--
-- PostgreSQL database dump
--

\restrict eyorXyi8sTUxpMTDhr685wHQce3IgF62MfaqcgKE6TPOiD1I27xEHLnPaDhpLfN

-- Dumped from database version 17.7
-- Dumped by pg_dump version 17.7

-- Started on 2025-12-02 21:10:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 57345)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 6435 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- TOC entry 3 (class 3079 OID 58432)
-- Name: postgis_raster; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_raster WITH SCHEMA public;


--
-- TOC entry 6436 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION postgis_raster; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_raster IS 'PostGIS raster types and functions';


--
-- TOC entry 315 (class 1255 OID 73733)
-- Name: get_district_by_water_body(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_district_by_water_body(water_body_name character varying) RETURNS TABLE(water_name character varying, district_name character varying, water_type character varying, flood_prone boolean)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        wb.water_name,
        ab.boundary_name as district_name,
        wb.water_type,
        wb.flood_prone
    FROM water_bodies wb
    JOIN administrative_boundaries ab ON wb.boundary_id = ab.boundary_id
    WHERE wb.water_name ILIKE '%' || water_body_name || '%';
END;
$$;


ALTER FUNCTION public.get_district_by_water_body(water_body_name character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 235 (class 1259 OID 65551)
-- Name: administrative_boundaries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administrative_boundaries (
    boundary_id integer NOT NULL,
    boundary_name character varying(100) NOT NULL,
    boundary_type character varying(50),
    boundary_code character varying(20),
    population integer,
    area_sqkm numeric(10,2),
    geom public.geometry(MultiPolygon,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.administrative_boundaries OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 65550)
-- Name: administrative_boundaries_boundary_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.administrative_boundaries_boundary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.administrative_boundaries_boundary_id_seq OWNER TO postgres;

--
-- TOC entry 6437 (class 0 OID 0)
-- Dependencies: 234
-- Name: administrative_boundaries_boundary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administrative_boundaries_boundary_id_seq OWNED BY public.administrative_boundaries.boundary_id;


--
-- TOC entry 239 (class 1259 OID 65574)
-- Name: disaster_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disaster_events (
    event_id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    event_date date NOT NULL,
    severity character varying(20),
    affected_area character varying(100),
    casualties integer DEFAULT 0,
    displaced_people integer DEFAULT 0,
    economic_loss_usd numeric(15,2),
    description text,
    geom public.geometry(Point,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.disaster_events OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 65573)
-- Name: disaster_events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.disaster_events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.disaster_events_event_id_seq OWNER TO postgres;

--
-- TOC entry 6438 (class 0 OID 0)
-- Dependencies: 238
-- Name: disaster_events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.disaster_events_event_id_seq OWNED BY public.disaster_events.event_id;


--
-- TOC entry 247 (class 1259 OID 65631)
-- Name: elevation_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.elevation_data (
    elevation_id integer NOT NULL,
    elevation_m numeric(8,2) NOT NULL,
    slope_degree numeric(5,2),
    aspect character varying(20),
    geom public.geometry(Point,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.elevation_data OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 65630)
-- Name: elevation_data_elevation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.elevation_data_elevation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.elevation_data_elevation_id_seq OWNER TO postgres;

--
-- TOC entry 6439 (class 0 OID 0)
-- Dependencies: 246
-- Name: elevation_data_elevation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.elevation_data_elevation_id_seq OWNED BY public.elevation_data.elevation_id;


--
-- TOC entry 251 (class 1259 OID 65654)
-- Name: evacuation_centers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.evacuation_centers (
    center_id integer NOT NULL,
    center_name character varying(100) NOT NULL,
    capacity integer NOT NULL,
    current_occupancy integer DEFAULT 0,
    facilities text,
    accessibility_score numeric(3,2),
    boundary_id integer,
    geom public.geometry(Point,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.evacuation_centers OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 65653)
-- Name: evacuation_centers_center_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.evacuation_centers_center_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.evacuation_centers_center_id_seq OWNER TO postgres;

--
-- TOC entry 6440 (class 0 OID 0)
-- Dependencies: 250
-- Name: evacuation_centers_center_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.evacuation_centers_center_id_seq OWNED BY public.evacuation_centers.center_id;


--
-- TOC entry 241 (class 1259 OID 65586)
-- Name: infrastructure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.infrastructure (
    infra_id integer NOT NULL,
    infra_name character varying(100) NOT NULL,
    infra_type character varying(50),
    capacity integer,
    operational_status character varying(20),
    vulnerability_score numeric(3,2),
    boundary_id integer,
    geom public.geometry(Point,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.infrastructure OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 65585)
-- Name: infrastructure_infra_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.infrastructure_infra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.infrastructure_infra_id_seq OWNER TO postgres;

--
-- TOC entry 6441 (class 0 OID 0)
-- Dependencies: 240
-- Name: infrastructure_infra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.infrastructure_infra_id_seq OWNED BY public.infrastructure.infra_id;


--
-- TOC entry 249 (class 1259 OID 65641)
-- Name: population_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.population_data (
    pop_id integer NOT NULL,
    census_year integer NOT NULL,
    total_population integer NOT NULL,
    male_population integer,
    female_population integer,
    households integer,
    vulnerable_population integer,
    boundary_id integer,
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.population_data OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 65640)
-- Name: population_data_pop_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.population_data_pop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.population_data_pop_id_seq OWNER TO postgres;

--
-- TOC entry 6442 (class 0 OID 0)
-- Dependencies: 248
-- Name: population_data_pop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.population_data_pop_id_seq OWNED BY public.population_data.pop_id;


--
-- TOC entry 243 (class 1259 OID 65601)
-- Name: rainfall_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rainfall_data (
    rainfall_id integer NOT NULL,
    station_name character varying(100),
    measurement_date date NOT NULL,
    rainfall_mm numeric(6,2) NOT NULL,
    boundary_id integer,
    geom public.geometry(Point,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.rainfall_data OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 65600)
-- Name: rainfall_data_rainfall_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rainfall_data_rainfall_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rainfall_data_rainfall_id_seq OWNER TO postgres;

--
-- TOC entry 6443 (class 0 OID 0)
-- Dependencies: 242
-- Name: rainfall_data_rainfall_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rainfall_data_rainfall_id_seq OWNED BY public.rainfall_data.rainfall_id;


--
-- TOC entry 245 (class 1259 OID 65616)
-- Name: risk_zones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.risk_zones (
    zone_id integer NOT NULL,
    zone_name character varying(100),
    risk_level character varying(20),
    risk_type character varying(50),
    affected_population integer,
    risk_score numeric(4,2),
    last_assessment_date date,
    boundary_id integer,
    geom public.geometry(MultiPolygon,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.risk_zones OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 65615)
-- Name: risk_zones_zone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.risk_zones_zone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.risk_zones_zone_id_seq OWNER TO postgres;

--
-- TOC entry 6444 (class 0 OID 0)
-- Dependencies: 244
-- Name: risk_zones_zone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.risk_zones_zone_id_seq OWNED BY public.risk_zones.zone_id;


--
-- TOC entry 253 (class 1259 OID 65670)
-- Name: soil_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.soil_data (
    soil_id integer NOT NULL,
    soil_type character varying(50),
    drainage_capacity character varying(20),
    permeability numeric(5,2),
    boundary_id integer,
    geom public.geometry(MultiPolygon,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.soil_data OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 65669)
-- Name: soil_data_soil_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.soil_data_soil_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.soil_data_soil_id_seq OWNER TO postgres;

--
-- TOC entry 6445 (class 0 OID 0)
-- Dependencies: 252
-- Name: soil_data_soil_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.soil_data_soil_id_seq OWNED BY public.soil_data.soil_id;


--
-- TOC entry 256 (class 1259 OID 65708)
-- Name: v_disaster_trends; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_disaster_trends AS
 SELECT EXTRACT(year FROM event_date) AS year,
    event_type,
    count(*) AS event_count,
    sum(casualties) AS total_casualties,
    sum(displaced_people) AS total_displaced,
    sum(economic_loss_usd) AS total_economic_loss
   FROM public.disaster_events
  GROUP BY (EXTRACT(year FROM event_date)), event_type
  ORDER BY (EXTRACT(year FROM event_date)) DESC, (count(*)) DESC;


ALTER VIEW public.v_disaster_trends OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 65563)
-- Name: water_bodies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.water_bodies (
    water_id integer NOT NULL,
    water_name character varying(100) NOT NULL,
    water_type character varying(50),
    length_km numeric(10,2),
    avg_width_m numeric(8,2),
    flood_prone boolean DEFAULT false,
    geom public.geometry(MultiLineString,4326),
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    boundary_id integer
);


ALTER TABLE public.water_bodies OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 73734)
-- Name: v_district_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_district_summary AS
 SELECT ab.boundary_name AS district,
    ab.boundary_code,
    ab.population,
    ab.area_sqkm,
    count(DISTINCT wb.water_id) AS num_water_bodies,
    count(DISTINCT de.event_id) AS num_disasters,
    sum(de.casualties) AS total_casualties,
    sum(de.displaced_people) AS total_displaced,
    round(sum(de.economic_loss_usd), 2) AS total_economic_loss
   FROM ((public.administrative_boundaries ab
     LEFT JOIN public.water_bodies wb ON ((ab.boundary_id = wb.boundary_id)))
     LEFT JOIN public.disaster_events de ON (((ab.boundary_name)::text = (de.affected_area)::text)))
  GROUP BY ab.boundary_id, ab.boundary_name, ab.boundary_code, ab.population, ab.area_sqkm
  ORDER BY ab.boundary_name;


ALTER VIEW public.v_district_summary OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 65712)
-- Name: v_evacuation_capacity; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_evacuation_capacity AS
 SELECT ab.boundary_name,
    ab.population,
    count(ec.center_id) AS num_centers,
    sum(ec.capacity) AS total_capacity,
    (ab.population - sum(ec.capacity)) AS capacity_gap,
    round((((sum(ec.capacity))::numeric / (ab.population)::numeric) * (100)::numeric), 2) AS coverage_percent
   FROM (public.administrative_boundaries ab
     LEFT JOIN public.evacuation_centers ec ON ((ab.boundary_id = ec.boundary_id)))
  GROUP BY ab.boundary_id, ab.boundary_name, ab.population
  ORDER BY (ab.population - sum(ec.capacity)) DESC;


ALTER VIEW public.v_evacuation_capacity OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 73739)
-- Name: v_flood_prone_districts; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_flood_prone_districts AS
 SELECT ab.boundary_name AS district,
    ab.population,
    count(DISTINCT de.event_id) AS flood_count,
    sum(de.displaced_people) AS total_displaced,
    string_agg(DISTINCT (wb.water_name)::text, ', '::text) AS flood_prone_rivers,
        CASE
            WHEN (count(DISTINCT de.event_id) >= 3) THEN 'EXTREME'::text
            WHEN (count(DISTINCT de.event_id) >= 2) THEN 'HIGH'::text
            WHEN (count(DISTINCT de.event_id) >= 1) THEN 'MEDIUM'::text
            ELSE 'LOW'::text
        END AS risk_level
   FROM ((public.administrative_boundaries ab
     LEFT JOIN public.disaster_events de ON ((((ab.boundary_name)::text = (de.affected_area)::text) AND ((de.event_type)::text = 'flood'::text))))
     LEFT JOIN public.water_bodies wb ON (((ab.boundary_id = wb.boundary_id) AND (wb.flood_prone = true))))
  GROUP BY ab.boundary_id, ab.boundary_name, ab.population
  ORDER BY (count(DISTINCT de.event_id)) DESC;


ALTER VIEW public.v_flood_prone_districts OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 65717)
-- Name: v_flood_prone_zones; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_flood_prone_zones AS
 SELECT wb.water_name,
    wb.water_type,
    wb.flood_prone,
    rz.zone_name,
    rz.risk_level,
    rz.affected_population,
    (public.st_distance((wb.geom)::public.geography, (rz.geom)::public.geography) / (1000)::double precision) AS distance_km
   FROM (public.water_bodies wb
     CROSS JOIN public.risk_zones rz)
  WHERE ((wb.flood_prone = true) AND public.st_dwithin((wb.geom)::public.geography, (rz.geom)::public.geography, (5000)::double precision))
  ORDER BY (public.st_distance((wb.geom)::public.geography, (rz.geom)::public.geography) / (1000)::double precision);


ALTER VIEW public.v_flood_prone_zones OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 65698)
-- Name: v_high_risk_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_high_risk_summary AS
 SELECT rz.zone_name,
    rz.risk_level,
    rz.risk_type,
    rz.affected_population,
    rz.risk_score,
    ab.boundary_name,
    ab.population AS total_district_population,
    round((((rz.affected_population)::numeric / (ab.population)::numeric) * (100)::numeric), 2) AS percent_affected
   FROM (public.risk_zones rz
     JOIN public.administrative_boundaries ab ON ((rz.boundary_id = ab.boundary_id)))
  WHERE ((rz.risk_level)::text = ANY ((ARRAY['high'::character varying, 'extreme'::character varying])::text[]))
  ORDER BY rz.risk_score DESC;


ALTER VIEW public.v_high_risk_summary OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 65703)
-- Name: v_infrastructure_at_risk; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_infrastructure_at_risk AS
 SELECT i.infra_name,
    i.infra_type,
    i.vulnerability_score,
    ab.boundary_name,
    rz.risk_level,
    rz.risk_type,
    (public.st_distance((i.geom)::public.geography, (rz.geom)::public.geography) / (1000)::double precision) AS distance_to_risk_km
   FROM ((public.infrastructure i
     JOIN public.administrative_boundaries ab ON ((i.boundary_id = ab.boundary_id)))
     LEFT JOIN public.risk_zones rz ON (public.st_intersects(i.geom, rz.geom)))
  WHERE ((i.vulnerability_score > 0.6) OR ((rz.risk_level)::text = ANY ((ARRAY['high'::character varying, 'extreme'::character varying])::text[])))
  ORDER BY i.vulnerability_score DESC;


ALTER VIEW public.v_infrastructure_at_risk OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 65562)
-- Name: water_bodies_water_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.water_bodies_water_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.water_bodies_water_id_seq OWNER TO postgres;

--
-- TOC entry 6446 (class 0 OID 0)
-- Dependencies: 236
-- Name: water_bodies_water_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.water_bodies_water_id_seq OWNED BY public.water_bodies.water_id;


--
-- TOC entry 6182 (class 2604 OID 65554)
-- Name: administrative_boundaries boundary_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrative_boundaries ALTER COLUMN boundary_id SET DEFAULT nextval('public.administrative_boundaries_boundary_id_seq'::regclass);


--
-- TOC entry 6187 (class 2604 OID 65577)
-- Name: disaster_events event_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disaster_events ALTER COLUMN event_id SET DEFAULT nextval('public.disaster_events_event_id_seq'::regclass);


--
-- TOC entry 6197 (class 2604 OID 65634)
-- Name: elevation_data elevation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elevation_data ALTER COLUMN elevation_id SET DEFAULT nextval('public.elevation_data_elevation_id_seq'::regclass);


--
-- TOC entry 6201 (class 2604 OID 65657)
-- Name: evacuation_centers center_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.evacuation_centers ALTER COLUMN center_id SET DEFAULT nextval('public.evacuation_centers_center_id_seq'::regclass);


--
-- TOC entry 6191 (class 2604 OID 65589)
-- Name: infrastructure infra_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infrastructure ALTER COLUMN infra_id SET DEFAULT nextval('public.infrastructure_infra_id_seq'::regclass);


--
-- TOC entry 6199 (class 2604 OID 65644)
-- Name: population_data pop_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.population_data ALTER COLUMN pop_id SET DEFAULT nextval('public.population_data_pop_id_seq'::regclass);


--
-- TOC entry 6193 (class 2604 OID 65604)
-- Name: rainfall_data rainfall_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rainfall_data ALTER COLUMN rainfall_id SET DEFAULT nextval('public.rainfall_data_rainfall_id_seq'::regclass);


--
-- TOC entry 6195 (class 2604 OID 65619)
-- Name: risk_zones zone_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.risk_zones ALTER COLUMN zone_id SET DEFAULT nextval('public.risk_zones_zone_id_seq'::regclass);


--
-- TOC entry 6204 (class 2604 OID 65673)
-- Name: soil_data soil_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soil_data ALTER COLUMN soil_id SET DEFAULT nextval('public.soil_data_soil_id_seq'::regclass);


--
-- TOC entry 6184 (class 2604 OID 65566)
-- Name: water_bodies water_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bodies ALTER COLUMN water_id SET DEFAULT nextval('public.water_bodies_water_id_seq'::regclass);


--
-- TOC entry 6411 (class 0 OID 65551)
-- Dependencies: 235
-- Data for Name: administrative_boundaries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrative_boundaries (boundary_id, boundary_name, boundary_type, boundary_code, population, area_sqkm, geom, created_date) FROM stdin;
7	Chitipa	district	MW-CT	234927	4288.00	0106000020E61000000100000001030000000100000005000000000000000080404066666666666623C03333333333B3404066666666666623C03333333333B3404066666666666624C0000000000080404066666666666624C0000000000080404066666666666623C0	2025-12-02 20:57:35.608025
8	Karonga	district	MW-KR	365028	3355.00	0106000020E610000001000000010300000001000000050000009A99999999D9404000000000000023C09A9999999919414000000000000023C09A9999999919414066666666666624C09A99999999D9404066666666666624C09A99999999D9404000000000000023C0	2025-12-02 20:57:35.608025
9	Likoma	district	MW-LK	14527	18.00	0106000020E610000001000000010300000001000000050000009A99999999594140CDCCCCCCCCCC27C06666666666664140CDCCCCCCCCCC27C0666666666666414033333333333328C09A9999999959414033333333333328C09A99999999594140CDCCCCCCCCCC27C0	2025-12-02 20:57:35.608025
10	Mzimba	district	MW-MZ	610944	10430.00	0106000020E610000001000000010300000001000000050000006666666666A6404000000000000026C0000000000000414000000000000026C0000000000000414066666666666628C06666666666A6404066666666666628C06666666666A6404000000000000026C0	2025-12-02 20:57:35.608025
11	Nkhata Bay	district	MW-NB	289780	4071.00	0106000020E610000001000000010300000001000000050000003333333333F3404066666666666626C0000000000040414066666666666626C0000000000040414000000000000028C03333333333F3404000000000000028C03333333333F3404066666666666626C0	2025-12-02 20:57:35.608025
12	Rumphi	district	MW-RU	197583	4769.00	0106000020E610000001000000010300000001000000050000000000000000C0404066666666666624C0000000000000414066666666666624C0000000000000414000000000000026C00000000000C0404000000000000026C00000000000C0404066666666666624C0	2025-12-02 20:57:35.608025
13	Dedza	district	MW-DE	830512	3624.00	0106000020E6100000010000000103000000010000000500000000000000000041409A99999999992BC0CDCCCCCCCC4C41409A99999999992BC0CDCCCCCCCC4C41400000000000002DC000000000000041400000000000002DC000000000000041409A99999999992BC0	2025-12-02 20:57:35.608025
14	Dowa	district	MW-DO	779203	3041.00	0106000020E61000000100000001030000000100000005000000CDCCCCCCCCCC4040CDCCCCCCCCCC2AC09A99999999194140CDCCCCCCCCCC2AC09A999999991941400000000000002CC0CDCCCCCCCCCC40400000000000002CC0CDCCCCCCCCCC4040CDCCCCCCCCCC2AC0	2025-12-02 20:57:35.608025
15	Kasungu	district	MW-KS	842953	7878.00	0106000020E61000000100000001030000000100000005000000666666666666404000000000000029C06666666666E6404000000000000029C06666666666E640400000000000002BC066666666666640400000000000002BC0666666666666404000000000000029C0	2025-12-02 20:57:35.608025
16	Lilongwe	district	MW-LI	2584055	6159.00	0106000020E610000001000000010300000001000000050000003333333333B340403333333333332BC09A999999991941403333333333332BC09A999999991941409A99999999992CC03333333333B340409A99999999992CC03333333333B340403333333333332BC0	2025-12-02 20:57:35.608025
17	Mchinji	district	MW-MC	602305	3356.00	0106000020E610000001000000010300000001000000050000009A999999995940400000000000002BC03333333333B340400000000000002BC03333333333B340406666666666662CC09A999999995940406666666666662CC09A999999995940400000000000002BC0	2025-12-02 20:57:35.608025
18	Nkhotakota	district	MW-NK	395897	4259.00	0106000020E610000001000000010300000001000000050000006666666666E6404000000000000029C0000000000040414000000000000029C000000000004041409A99999999992AC06666666666E640409A99999999992AC06666666666E6404000000000000029C0	2025-12-02 20:57:35.608025
19	Ntcheu	district	MW-NU	659186	3424.00	0106000020E6100000010000000103000000010000000500000000000000004041400000000000002DC09A999999999941400000000000002DC09A999999999941409A99999999992EC000000000004041409A99999999992EC000000000004041400000000000002DC0	2025-12-02 20:57:35.608025
20	Ntchisi	district	MW-NI	317069	1655.00	0106000020E610000001000000010300000001000000050000006666666666E640406666666666662AC09A999999991941406666666666662AC09A999999991941403333333333332BC06666666666E640403333333333332BC06666666666E640406666666666662AC0	2025-12-02 20:57:35.608025
21	Salima	district	MW-SA	478346	2196.00	0106000020E61000000100000001030000000100000005000000CDCCCCCCCC0C41400000000000002BC09A999999995941400000000000002BC09A999999995941400000000000002CC0CDCCCCCCCC0C41400000000000002CC0CDCCCCCCCC0C41400000000000002BC0	2025-12-02 20:57:35.608025
22	Balaka	district	MW-BA	428801	2193.00	0106000020E6100000010000000103000000010000000500000066666666666641406666666666662DC06666666666A641406666666666662DC06666666666A641406666666666662EC066666666666641406666666666662EC066666666666641406666666666662DC0	2025-12-02 20:57:35.608025
23	Blantyre	district	MW-BL	1316250	2012.00	0106000020E6100000010000000103000000010000000500000066666666666641400000000000002FC09A999999999941400000000000002FC09A9999999999414000000000000030C0666666666666414000000000000030C066666666666641400000000000002FC0	2025-12-02 20:57:35.608025
24	Chikwawa	district	MW-CK	564684	4755.00	0106000020E6100000010000000103000000010000000500000000000000004041409A99999999992FC09A999999999941409A99999999992FC09A99999999994140CDCCCCCCCCCC30C00000000000404140CDCCCCCCCCCC30C000000000004041409A99999999992FC0	2025-12-02 20:57:35.608025
25	Chiradzulu	district	MW-CR	356875	767.00	0106000020E61000000100000001030000000100000005000000CDCCCCCCCC8C41400000000000002FC03333333333B341400000000000002FC03333333333B34140CDCCCCCCCCCC2FC0CDCCCCCCCC8C4140CDCCCCCCCCCC2FC0CDCCCCCCCC8C41400000000000002FC0	2025-12-02 20:57:35.608025
26	Machinga	district	MW-MA	602749	3771.00	0106000020E610000001000000010300000001000000050000009A999999999941409A99999999992DC06666666666E641409A99999999992DC06666666666E641400000000000002FC09A999999999941400000000000002FC09A999999999941409A99999999992DC0	2025-12-02 20:57:35.608025
27	Mangochi	district	MW-MG	1018302	6273.00	0106000020E6100000010000000103000000010000000500000066666666666641400000000000002CC0CDCCCCCCCCCC41400000000000002CC0CDCCCCCCCCCC41409A99999999992DC066666666666641409A99999999992DC066666666666641400000000000002CC0	2025-12-02 20:57:35.608025
28	Mulanje	district	MW-MU	684107	2056.00	0106000020E610000001000000010300000001000000050000006666666666A641406666666666662FC06666666666E641406666666666662FC06666666666E6414033333333333330C06666666666A6414033333333333330C06666666666A641406666666666662FC0	2025-12-02 20:57:35.608025
29	Mwanza	district	MW-MW	104256	2259.00	0106000020E610000001000000010300000001000000050000006666666666264140CDCCCCCCCCCC2EC06666666666664140CDCCCCCCCCCC2EC06666666666664140CDCCCCCCCCCC2FC06666666666264140CDCCCCCCCCCC2FC06666666666264140CDCCCCCCCCCC2EC0	2025-12-02 20:57:35.608025
30	Nsanje	district	MW-NS	299168	1942.00	0106000020E61000000100000001030000000100000005000000333333333373414000000000008030C03333333333B3414000000000008030C03333333333B3414000000000000031C0333333333373414000000000000031C0333333333373414000000000008030C0	2025-12-02 20:57:35.608025
31	Phalombe	district	MW-PH	403346	1394.00	0106000020E610000001000000010300000001000000050000000000000000C041400000000000002FC03333333333F341400000000000002FC03333333333F3414000000000000030C00000000000C0414000000000000030C00000000000C041400000000000002FC0	2025-12-02 20:57:35.608025
32	Thyolo	district	MW-TH	721456	1715.00	0106000020E610000001000000010300000001000000050000000000000000804140CDCCCCCCCCCC2FC03333333333B34140CDCCCCCCCCCC2FC03333333333B3414066666666666630C0000000000080414066666666666630C00000000000804140CDCCCCCCCCCC2FC0	2025-12-02 20:57:35.608025
33	Zomba	district	MW-ZO	851845	2580.00	0106000020E610000001000000010300000001000000050000009A999999999941406666666666662EC09A99999999D941406666666666662EC09A99999999D941406666666666662FC09A999999999941406666666666662FC09A999999999941406666666666662EC0	2025-12-02 20:57:35.608025
34	Neno	district	MW-NE	156742	1567.00	0106000020E6100000010000000103000000010000000500000000000000004041406666666666662EC033333333337341406666666666662EC033333333337341406666666666662FC000000000004041406666666666662FC000000000004041406666666666662EC0	2025-12-02 20:57:35.608025
\.


--
-- TOC entry 6415 (class 0 OID 65574)
-- Dependencies: 239
-- Data for Name: disaster_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.disaster_events (event_id, event_type, event_date, severity, affected_area, casualties, displaced_people, economic_loss_usd, description, geom, created_date) FROM stdin;
61	flood	2024-01-15	extreme	Zomba	45	12000	5500000.00	Severe flooding in Zomba district due to heavy rainfall	0101000020E6100000295C8FC2F5A84140C3F5285C8FC22EC0	2025-12-02 20:59:42.113006
62	cyclone	2023-03-15	extreme	Blantyre	67	15000	8900000.00	Tropical Cyclone Freddy impact on Blantyre	0101000020E6100000000000000080414014AE47E17A942FC0	2025-12-02 20:59:42.113006
63	flood	2023-03-20	high	Nsanje	28	8500	3200000.00	River overflow caused widespread damage in Nsanje	0101000020E6100000E17A14AE47A14140EC51B81E85EB30C0	2025-12-02 20:59:42.113006
64	flood	2022-01-22	high	Chikwawa	38	9800	4100000.00	Shire River flooding in Chikwawa	0101000020E610000085EB51B81E65414048E17A14AE0730C0	2025-12-02 20:59:42.113006
65	flood	2021-03-14	extreme	Phalombe	52	11500	6700000.00	Major flooding from tropical storm in Phalombe	0101000020E61000003333333333D341409A99999999992FC0	2025-12-02 20:59:42.113006
66	cyclone	2021-02-28	high	Mulanje	41	13200	7200000.00	Cyclone Ana caused extensive damage in Mulanje	0101000020E61000000000000000C0414048E17A14AE0730C0	2025-12-02 20:59:42.113006
67	flood	2019-03-07	extreme	Zomba	89	18700	12500000.00	Cyclone Idai - worst disaster in Zomba	0101000020E610000048E17A14AEA7414048E17A14AEC72EC0	2025-12-02 20:59:42.113006
68	flood	2019-03-08	extreme	Chiradzulu	76	16200	11800000.00	Cyclone Idai impact on Chiradzulu	0101000020E61000001F85EB51B89E41405C8FC2F5285C2FC0	2025-12-02 20:59:42.113006
69	flood	2019-03-09	extreme	Nsanje	102	21000	15200000.00	Cyclone Idai devastates Nsanje - worst hit area	0101000020E61000000000000000A04140AE47E17A14EE30C0	2025-12-02 20:59:42.113006
70	landslide	2022-11-18	high	Thyolo	34	2100	1200000.00	Heavy rains triggered landslides in Thyolo hills	0101000020E610000052B81E85EB91414052B81E85EB1130C0	2025-12-02 20:59:42.113006
71	drought	2021-09-30	medium	Kasungu	0	0	2500000.00	Agricultural drought affecting crops in Kasungu	0101000020E61000003D0AD7A370BD40408FC2F5285C0F2AC0	2025-12-02 20:59:42.113006
72	flood	2020-12-19	medium	Salima	15	5300	2100000.00	Localized flooding in low-lying areas of Salima	0101000020E61000009A999999993941408FC2F5285C8F2BC0	2025-12-02 20:59:42.113006
73	earthquake	2020-07-11	low	Karonga	3	150	250000.00	Minor earthquake in Karonga, minimal damage	0101000020E6100000D7A3703D0AF740405C8FC2F528DC23C0	2025-12-02 20:59:42.113006
74	flood	2018-02-14	high	Mzimba	24	6800	2800000.00	Urban flash flooding in Mzimba	0101000020E6100000CDCCCCCCCCCC4040CDCCCCCCCCCC27C0	2025-12-02 20:59:42.113006
75	drought	2017-10-01	high	Mchinji	0	0	4200000.00	Severe agricultural drought in Mchinji	0101000020E610000000000000008040409A99999999992BC0	2025-12-02 20:59:42.113006
76	flood	2017-01-28	medium	Machinga	19	4900	1900000.00	River flooding in rural Machinga	0101000020E6100000C3F5285C8FC24140B81E85EB51382EC0	2025-12-02 20:59:42.113006
77	cyclone	2016-03-05	high	Mangochi	36	10200	5800000.00	Tropical storm caused flooding in Mangochi	0101000020E6100000E17A14AE47A14140F6285C8FC2F52CC0	2025-12-02 20:59:42.113006
78	flood	2015-12-11	medium	Lilongwe	14	3800	1600000.00	December rains caused flooding in Lilongwe	0101000020E6100000A4703D0AD7E34040F6285C8FC2F52BC0	2025-12-02 20:59:42.113006
79	landslide	2015-04-22	low	Dedza	3	180	340000.00	Small-scale landslides in Dedza	0101000020E61000000AD7A3703D2A4140C3F5285C8FC22CC0	2025-12-02 20:59:42.113006
80	flood	2022-12-05	medium	Nkhata Bay	12	4200	1800000.00	Flash floods in Nkhata Bay urban areas	0101000020E6100000666666666626414033333333333327C0	2025-12-02 20:59:42.113006
\.


--
-- TOC entry 6423 (class 0 OID 65631)
-- Dependencies: 247
-- Data for Name: elevation_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.elevation_data (elevation_id, elevation_m, slope_degree, aspect, geom, created_date) FROM stdin;
1	450.50	2.30	N	0101000020E610000000000000002041400000000000802AC0	2025-12-02 20:09:54.724643
2	520.80	5.70	NE	0101000020E610000000000000006041400000000000802AC0	2025-12-02 20:09:54.724643
3	380.20	1.80	E	0101000020E6100000000000000020414000000000008029C0	2025-12-02 20:09:54.724643
4	410.30	3.20	SE	0101000020E610000000000000002041400000000000802BC0	2025-12-02 20:09:54.724643
5	395.70	8.40	W	0101000020E61000000000000000E040400000000000802AC0	2025-12-02 20:09:54.724643
6	450.50	2.30	N	0101000020E610000000000000002041400000000000802AC0	2025-12-02 20:24:04.971875
7	520.80	5.70	NE	0101000020E610000000000000006041400000000000802AC0	2025-12-02 20:24:04.971875
8	380.20	1.80	E	0101000020E6100000000000000020414000000000008029C0	2025-12-02 20:24:04.971875
9	410.30	3.20	SE	0101000020E610000000000000002041400000000000802BC0	2025-12-02 20:24:04.971875
10	395.70	8.40	W	0101000020E61000000000000000E040400000000000802AC0	2025-12-02 20:24:04.971875
11	450.50	2.30	N	0101000020E610000000000000002041400000000000802AC0	2025-12-02 20:25:50.641005
12	520.80	5.70	NE	0101000020E610000000000000006041400000000000802AC0	2025-12-02 20:25:50.641005
13	380.20	1.80	E	0101000020E6100000000000000020414000000000008029C0	2025-12-02 20:25:50.641005
14	410.30	3.20	SE	0101000020E610000000000000002041400000000000802BC0	2025-12-02 20:25:50.641005
15	395.70	8.40	W	0101000020E61000000000000000E040400000000000802AC0	2025-12-02 20:25:50.641005
16	475.20	4.10	S	0101000020E610000066666666662641409A99999999992AC0	2025-12-02 20:25:50.641005
17	505.90	6.30	SW	0101000020E61000009A999999991941409A99999999992AC0	2025-12-02 20:25:50.641005
18	425.60	2.90	NW	0101000020E61000009A999999991941406666666666662AC0	2025-12-02 20:25:50.641005
19	440.10	3.50	N	0101000020E610000066666666662641406666666666662AC0	2025-12-02 20:25:50.641005
20	488.30	5.20	NE	0101000020E6100000CDCCCCCCCC2C41400000000000802AC0	2025-12-02 20:25:50.641005
21	402.70	2.10	E	0101000020E610000066666666662641409A999999999929C0	2025-12-02 20:25:50.641005
22	455.80	4.80	SE	0101000020E610000066666666662641409A99999999992BC0	2025-12-02 20:25:50.641005
23	390.50	7.60	W	0101000020E61000009A99999999D940409A99999999992AC0	2025-12-02 20:25:50.641005
24	512.40	6.90	S	0101000020E610000066666666666641409A99999999992AC0	2025-12-02 20:25:50.641005
25	468.90	3.70	SW	0101000020E61000009A999999991941406666666666662BC0	2025-12-02 20:25:50.641005
26	450.50	2.30	N	0101000020E610000000000000002041400000000000802AC0	2025-12-02 20:42:33.728184
27	520.80	5.70	NE	0101000020E610000000000000006041400000000000802AC0	2025-12-02 20:42:33.728184
28	380.20	1.80	E	0101000020E6100000000000000020414000000000008029C0	2025-12-02 20:42:33.728184
29	410.30	3.20	SE	0101000020E610000000000000002041400000000000802BC0	2025-12-02 20:42:33.728184
30	395.70	8.40	W	0101000020E61000000000000000E040400000000000802AC0	2025-12-02 20:42:33.728184
31	475.20	4.10	S	0101000020E610000066666666662641409A99999999992AC0	2025-12-02 20:42:33.728184
32	505.90	6.30	SW	0101000020E61000009A999999991941409A99999999992AC0	2025-12-02 20:42:33.728184
33	425.60	2.90	NW	0101000020E61000009A999999991941406666666666662AC0	2025-12-02 20:42:33.728184
34	440.10	3.50	N	0101000020E610000066666666662641406666666666662AC0	2025-12-02 20:42:33.728184
35	488.30	5.20	NE	0101000020E6100000CDCCCCCCCC2C41400000000000802AC0	2025-12-02 20:42:33.728184
36	402.70	2.10	E	0101000020E610000066666666662641409A999999999929C0	2025-12-02 20:42:33.728184
37	455.80	4.80	SE	0101000020E610000066666666662641409A99999999992BC0	2025-12-02 20:42:33.728184
38	390.50	7.60	W	0101000020E61000009A99999999D940409A99999999992AC0	2025-12-02 20:42:33.728184
39	512.40	6.90	S	0101000020E610000066666666666641409A99999999992AC0	2025-12-02 20:42:33.728184
40	468.90	3.70	SW	0101000020E61000009A999999991941406666666666662BC0	2025-12-02 20:42:33.728184
\.


--
-- TOC entry 6427 (class 0 OID 65654)
-- Dependencies: 251
-- Data for Name: evacuation_centers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.evacuation_centers (center_id, center_name, capacity, current_occupancy, facilities, accessibility_score, boundary_id, geom, created_date) FROM stdin;
\.


--
-- TOC entry 6417 (class 0 OID 65586)
-- Dependencies: 241
-- Data for Name: infrastructure; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.infrastructure (infra_id, infra_name, infra_type, capacity, operational_status, vulnerability_score, boundary_id, geom, created_date) FROM stdin;
\.


--
-- TOC entry 6425 (class 0 OID 65641)
-- Dependencies: 249
-- Data for Name: population_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.population_data (pop_id, census_year, total_population, male_population, female_population, households, vulnerable_population, boundary_id, created_date) FROM stdin;
\.


--
-- TOC entry 6419 (class 0 OID 65601)
-- Dependencies: 243
-- Data for Name: rainfall_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rainfall_data (rainfall_id, station_name, measurement_date, rainfall_mm, boundary_id, geom, created_date) FROM stdin;
\.


--
-- TOC entry 6421 (class 0 OID 65616)
-- Dependencies: 245
-- Data for Name: risk_zones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.risk_zones (zone_id, zone_name, risk_level, risk_type, affected_population, risk_score, last_assessment_date, boundary_id, geom, created_date) FROM stdin;
\.


--
-- TOC entry 6429 (class 0 OID 65670)
-- Dependencies: 253
-- Data for Name: soil_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.soil_data (soil_id, soil_type, drainage_capacity, permeability, boundary_id, geom, created_date) FROM stdin;
\.


--
-- TOC entry 6181 (class 0 OID 57664)
-- Dependencies: 220
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- TOC entry 6413 (class 0 OID 65563)
-- Dependencies: 237
-- Data for Name: water_bodies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.water_bodies (water_id, water_name, water_type, length_km, avg_width_m, flood_prone, geom, created_date, boundary_id) FROM stdin;
19	Shire River	river	402.00	150.00	t	0105000020E61000000100000001020000000400000066666666666641403333333333332EC033333333337341400000000000002FC0000000000080414000000000000030C0CDCCCCCCCC8C414000000000008030C0	2025-12-02 20:59:13.041419	24
20	Lake Malawi	lake	560.00	50000.00	f	0105000020E610000001000000010200000005000000000000000040414000000000000024C0666666666666414000000000000026C0000000000080414000000000000028C09A999999999941400000000000002AC06666666666A641400000000000002CC0	2025-12-02 20:59:13.041419	27
21	Lake Chilwa	lake	0.00	1800.00	t	0105000020E610000001000000010200000005000000CDCCCCCCCCCC41406666666666662EC06666666666E641406666666666662EC06666666666E64140CDCCCCCCCCCC2EC0CDCCCCCCCCCC4140CDCCCCCCCCCC2EC0CDCCCCCCCCCC41406666666666662EC0	2025-12-02 20:59:13.041419	33
22	Ruo River	river	185.00	80.00	t	0105000020E610000001000000010200000003000000CDCCCCCCCCCC414000000000000030C00000000000C041409A99999999992FC03333333333B341403333333333332FC0	2025-12-02 20:59:13.041419	28
23	Likangala River	river	45.00	20.00	t	0105000020E6100000010000000102000000040000006666666666A641409A99999999992EC03333333333B34140CDCCCCCCCCCC2EC00000000000C041400000000000002FC0CDCCCCCCCCCC41403333333333332FC0	2025-12-02 20:59:13.041419	33
24	Bua River	river	200.00	60.00	t	0105000020E6100000010000000102000000030000003333333333F340409A999999999929C0CDCCCCCCCC0C41400000000000002AC066666666662641406666666666662AC0	2025-12-02 20:59:13.041419	18
25	Dwangwa River	river	120.00	45.00	f	0105000020E61000000100000001020000000300000000000000000041409A999999999928C09A9999999919414000000000000029C0333333333333414066666666666629C0	2025-12-02 20:59:13.041419	18
26	Songwe River	river	180.00	65.00	f	0105000020E6100000010000000102000000030000006666666666E6404033333333333323C03333333333F340409A999999999923C0000000000000414000000000000024C0	2025-12-02 20:59:13.041419	8
\.


--
-- TOC entry 6447 (class 0 OID 0)
-- Dependencies: 234
-- Name: administrative_boundaries_boundary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administrative_boundaries_boundary_id_seq', 34, true);


--
-- TOC entry 6448 (class 0 OID 0)
-- Dependencies: 238
-- Name: disaster_events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.disaster_events_event_id_seq', 80, true);


--
-- TOC entry 6449 (class 0 OID 0)
-- Dependencies: 246
-- Name: elevation_data_elevation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.elevation_data_elevation_id_seq', 40, true);


--
-- TOC entry 6450 (class 0 OID 0)
-- Dependencies: 250
-- Name: evacuation_centers_center_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.evacuation_centers_center_id_seq', 26, true);


--
-- TOC entry 6451 (class 0 OID 0)
-- Dependencies: 240
-- Name: infrastructure_infra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.infrastructure_infra_id_seq', 30, true);


--
-- TOC entry 6452 (class 0 OID 0)
-- Dependencies: 248
-- Name: population_data_pop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.population_data_pop_id_seq', 30, true);


--
-- TOC entry 6453 (class 0 OID 0)
-- Dependencies: 242
-- Name: rainfall_data_rainfall_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rainfall_data_rainfall_id_seq', 33, true);


--
-- TOC entry 6454 (class 0 OID 0)
-- Dependencies: 244
-- Name: risk_zones_zone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.risk_zones_zone_id_seq', 17, true);


--
-- TOC entry 6455 (class 0 OID 0)
-- Dependencies: 252
-- Name: soil_data_soil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.soil_data_soil_id_seq', 20, true);


--
-- TOC entry 6456 (class 0 OID 0)
-- Dependencies: 236
-- Name: water_bodies_water_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.water_bodies_water_id_seq', 26, true);


--
-- TOC entry 6210 (class 2606 OID 65561)
-- Name: administrative_boundaries administrative_boundaries_boundary_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrative_boundaries
    ADD CONSTRAINT administrative_boundaries_boundary_code_key UNIQUE (boundary_code);


--
-- TOC entry 6212 (class 2606 OID 65559)
-- Name: administrative_boundaries administrative_boundaries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrative_boundaries
    ADD CONSTRAINT administrative_boundaries_pkey PRIMARY KEY (boundary_id);


--
-- TOC entry 6218 (class 2606 OID 65584)
-- Name: disaster_events disaster_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disaster_events
    ADD CONSTRAINT disaster_events_pkey PRIMARY KEY (event_id);


--
-- TOC entry 6234 (class 2606 OID 65639)
-- Name: elevation_data elevation_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elevation_data
    ADD CONSTRAINT elevation_data_pkey PRIMARY KEY (elevation_id);


--
-- TOC entry 6239 (class 2606 OID 65663)
-- Name: evacuation_centers evacuation_centers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.evacuation_centers
    ADD CONSTRAINT evacuation_centers_pkey PRIMARY KEY (center_id);


--
-- TOC entry 6225 (class 2606 OID 65594)
-- Name: infrastructure infrastructure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infrastructure
    ADD CONSTRAINT infrastructure_pkey PRIMARY KEY (infra_id);


--
-- TOC entry 6237 (class 2606 OID 65647)
-- Name: population_data population_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.population_data
    ADD CONSTRAINT population_data_pkey PRIMARY KEY (pop_id);


--
-- TOC entry 6228 (class 2606 OID 65609)
-- Name: rainfall_data rainfall_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rainfall_data
    ADD CONSTRAINT rainfall_data_pkey PRIMARY KEY (rainfall_id);


--
-- TOC entry 6232 (class 2606 OID 65624)
-- Name: risk_zones risk_zones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.risk_zones
    ADD CONSTRAINT risk_zones_pkey PRIMARY KEY (zone_id);


--
-- TOC entry 6243 (class 2606 OID 65678)
-- Name: soil_data soil_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soil_data
    ADD CONSTRAINT soil_data_pkey PRIMARY KEY (soil_id);


--
-- TOC entry 6216 (class 2606 OID 65572)
-- Name: water_bodies water_bodies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bodies
    ADD CONSTRAINT water_bodies_pkey PRIMARY KEY (water_id);


--
-- TOC entry 6213 (class 1259 OID 65684)
-- Name: idx_admin_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_admin_geom ON public.administrative_boundaries USING gist (geom);


--
-- TOC entry 6219 (class 1259 OID 65693)
-- Name: idx_disaster_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_disaster_date ON public.disaster_events USING btree (event_date);


--
-- TOC entry 6220 (class 1259 OID 65686)
-- Name: idx_disaster_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_disaster_geom ON public.disaster_events USING gist (geom);


--
-- TOC entry 6221 (class 1259 OID 65694)
-- Name: idx_disaster_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_disaster_type ON public.disaster_events USING btree (event_type);


--
-- TOC entry 6235 (class 1259 OID 65690)
-- Name: idx_elevation_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_elevation_geom ON public.elevation_data USING gist (geom);


--
-- TOC entry 6240 (class 1259 OID 65691)
-- Name: idx_evacuation_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_evacuation_geom ON public.evacuation_centers USING gist (geom);


--
-- TOC entry 6222 (class 1259 OID 65687)
-- Name: idx_infra_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_infra_geom ON public.infrastructure USING gist (geom);


--
-- TOC entry 6223 (class 1259 OID 65695)
-- Name: idx_infra_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_infra_type ON public.infrastructure USING btree (infra_type);


--
-- TOC entry 6226 (class 1259 OID 65688)
-- Name: idx_rainfall_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_rainfall_geom ON public.rainfall_data USING gist (geom);


--
-- TOC entry 6229 (class 1259 OID 65689)
-- Name: idx_risk_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_risk_geom ON public.risk_zones USING gist (geom);


--
-- TOC entry 6230 (class 1259 OID 65696)
-- Name: idx_risk_level; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_risk_level ON public.risk_zones USING btree (risk_level);


--
-- TOC entry 6241 (class 1259 OID 65692)
-- Name: idx_soil_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_soil_geom ON public.soil_data USING gist (geom);


--
-- TOC entry 6214 (class 1259 OID 65685)
-- Name: idx_water_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_water_geom ON public.water_bodies USING gist (geom);


--
-- TOC entry 6249 (class 2606 OID 65664)
-- Name: evacuation_centers evacuation_centers_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.evacuation_centers
    ADD CONSTRAINT evacuation_centers_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6245 (class 2606 OID 65595)
-- Name: infrastructure infrastructure_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.infrastructure
    ADD CONSTRAINT infrastructure_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6248 (class 2606 OID 65648)
-- Name: population_data population_data_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.population_data
    ADD CONSTRAINT population_data_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6246 (class 2606 OID 65610)
-- Name: rainfall_data rainfall_data_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rainfall_data
    ADD CONSTRAINT rainfall_data_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6247 (class 2606 OID 65625)
-- Name: risk_zones risk_zones_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.risk_zones
    ADD CONSTRAINT risk_zones_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6250 (class 2606 OID 65679)
-- Name: soil_data soil_data_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soil_data
    ADD CONSTRAINT soil_data_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


--
-- TOC entry 6244 (class 2606 OID 73728)
-- Name: water_bodies water_bodies_boundary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bodies
    ADD CONSTRAINT water_bodies_boundary_id_fkey FOREIGN KEY (boundary_id) REFERENCES public.administrative_boundaries(boundary_id);


-- Completed on 2025-12-02 21:10:30

--
-- PostgreSQL database dump complete
--

\unrestrict eyorXyi8sTUxpMTDhr685wHQce3IgF62MfaqcgKE6TPOiD1I27xEHLnPaDhpLfN

