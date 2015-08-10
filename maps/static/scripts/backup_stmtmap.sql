--
-- PostgreSQL database dump
--

INSERT INTO stmtmap_article VALUES (4, 'none', 'Laminar differences in receptive field properties of cells in cat primary visual cortex', 'Gilbert CD', 'J Physiol (Lond) ', 1975, NULL, NULL, 1, false);
INSERT INTO stmtmap_article VALUES (5, 'none', 'Orientation Selectivity in Macaque V1: Diversity and Laminar Dependence', 'Dario L. Ringach, Robert M. Shapley, and Michael J. Hawken', 'The Journal of Neuroscience', 2002, NULL, NULL, 1, false);
INSERT INTO stmtmap_article VALUES (6, '0042-6989/02', 'On the classification of simple and complex cells', 'Ferenc Mechler, Dario L. Ringach', 'Vision Research', 2002, NULL, NULL, 1, false);
INSERT INTO stmtmap_article VALUES (3, ' http://dx.doi.org/10.1016/0042-6989(91)90033-2', 'Classifying simple and complex cells on the basis of response modulation', 'Bernt C. Skottun,Russell L. De Valois,David H. Grosof,J. Anthony Movshon,Duane G. Albrecht,A.B. Bonds', 'Vision Research', 1991, NULL, NULL, 1, false);
INSERT INTO stmtmap_article VALUES (7, '10.1126/science.287.5456.1273 ', 'Sparse Coding and Decorrelation in Primary Visual Cortex During Natural Vision', 'William E. Vinje, Jack L. Gallant', 'Science', 1999, NULL, NULL, 1, false);


--
-- TOC entry 1881 (class 0 OID 16585)
-- Dependencies: 168 1879
-- Data for Name: stmtmap_evidence; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO stmtmap_evidence VALUES (3, 3, '', 'Distribution of modulation ratio in Cat V1 is bimodal', 1, false);
INSERT INTO stmtmap_evidence VALUES (5, 5, '', 'The average modulation ratio in layer 4C is higher that in layer 2/3 in Macaque', 1, false);
INSERT INTO stmtmap_evidence VALUES (6, 7, '', 'The vm of pyramidal cells in V1 does not have bimodal distribution of modulation ratios', 1, false);
INSERT INTO stmtmap_evidence VALUES (7, 7, '', 'Stimulation of the non-classical receptive field in freeviewing macaque monkey (with natural images) increases sparsness and decorelates response of V1 neurons', 1, false);
INSERT INTO stmtmap_evidence VALUES (4, 4, '', 'In cat layer 4C contains mostly simple cells, and layer 2/3 complex cells', 1, false);


--
-- TOC entry 1878 (class 0 OID 16546)
-- Dependencies: 162
-- Data for Name: stmtmap_statement; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO stmtmap_statement VALUES (6, 'V1 contains 2 main functional types of cells: simple and complex', 'simple cells respond largely linearly to stimuli while complex cells show non-linear responses. A typical example of this is that simple cells prefer specific phase of a drifted grating, while response of complex cells tends to be phase invariant.', NULL, 1, false);
INSERT INTO stmtmap_statement VALUES (7, 'Layer 4 contains predominantely simple cells while layer 2/3 contains pre-dominantly complex cells.', 'The distribution of simple-complex types is non-even across layers. This supports the hierarchical model proposed by Hubel and Wiesel proposing that simple cells pool information from thalamus while complex cells pool information from other complex cells. Because layer 4C get most of the thalamic input arriving to V1, while layer 2/3 get input from layer 4C, according to the above theory, one would expect more simple cells in layer 4C and more complex cells in layer 2/3, in line with the evidence.', NULL, 1, false);
INSERT INTO stmtmap_statement VALUES (8, 'Simple and Complex cell types do not imply distinct underlying physiological cell types', 'Even though the modulation ratio of spiking responses is bimodal this does not imply that there are two separate physiological cell types in V1. ', NULL, 1, false);
INSERT INTO stmtmap_statement VALUES (9, 'Cells in cat V1 respond more accurately to natural images than drifting-gratings', '', NULL, 1, false);
INSERT INTO stmtmap_statement VALUES (10, 'Sparseness of V1 neural response is increased by addition of surround to CRF stimulation.', '', NULL, 1, false);


--
-- TOC entry 1880 (class 0 OID 16570)
-- Dependencies: 166 1878 1881
-- Data for Name: stmtmap_evidence_statements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO stmtmap_evidence_statements VALUES (11, 3, 6);
INSERT INTO stmtmap_evidence_statements VALUES (13, 5, 7);
INSERT INTO stmtmap_evidence_statements VALUES (22, 6, 8);
INSERT INTO stmtmap_evidence_statements VALUES (43, 7, 10);
INSERT INTO stmtmap_evidence_statements VALUES (46, 4, 9);
INSERT INTO stmtmap_evidence_statements VALUES (48, 4, 7);



