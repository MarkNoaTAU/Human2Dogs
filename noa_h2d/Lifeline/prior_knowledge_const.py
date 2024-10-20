"""
    Extracting taxa with significant assosiation from the suplementry table of the article:
    
    https://www.ahajournals.org/doi/10.1161/CIRCRESAHA.115.306807#sec-2
"""


taxa_signicantly_assosiated_with_bmi = ['k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Collinsella;s__stercoris',
                                        'k__Bacteria;p__Actinobacteria;c__Coriobacteriia;o__Coriobacteriales;f__Coriobacteriaceae;g__Eggerthell',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae;g__Bacteroides',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Bacteroidaceae/Rikenellaceae', # note, here they possibly aggregated together two correlated taxa, check?
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Odoribacteraceae',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Odoribacteraceae;g__Butyricimonas',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Odoribacteraceae;g__Odoribacter',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__Rikenellaceae',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__S24E7',
                                        'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__S24E7/Barnesiellaceae',  # note, here they possibly aggregated together two correlated taxa, check?
                                        'k__Bacteria;p__Cyanobacteria',
                                        'k__Bacteria;p__Firmicutes;c__Bacilli;o__Gemellales/Bacillales',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Christensenellaceae',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae;g__02d06',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Clostridiaceae/Lachnospiraceae',  # note,
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Dehalobacteriaceae;g__Dehalobacterium',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__Blautia 51',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__Coprococcu',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Lachnospiraceae;g__Lachnospira',
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Mogibacteriaceae/Clostridiaceae/Lachnospiraceae',  # note,
                                        'k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Peptostreptococcaceae/Mogibacteriaceae/Clostridiaceae',  # note,
                                        'k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__cc_115',
                                        'k__Bacteria;p__Firmicutes;c__Erysipelotrichi;o__Erysipelotrichales;f__Erysipelotrichaceae;g__Holdemani',
                                        'k__Bacteria;p__Proteobacteria;c__Betaproteobacteria;o__Burkholderiales/Rhodocyclales',  # note,
                                        'k__Bacteria;p__Proteobacteria;c__Deltaproteobacteria;o__Desulfovibrionales;f__Desulfovibrionaceae',
                                        'k__Bacteria;p__Proteobacteria;c__Deltaproteobacteria;o__Desulfovibrionales;f__Desulfovibrionaceae;g__Bilophila',
                                        'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria',
                                        'k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Pasteurellales;f__Pasteurellaceae',
                                        'k__Bacteria;p__Tenericutes',
                                        'k__Bacteria;p__Verrucomicrobia;c__Verrucomicrobiae;o__Verrucomicrobiales;f__Verrucomicrobiaceae;g__Akkermansia']


# TODO: Similary complete:
taxa_signicantly_assosiated_with_triglyceride = []
