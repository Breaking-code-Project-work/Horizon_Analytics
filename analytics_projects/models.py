from django.db import models

class Project(models.Model):

    # Enum project status
    class ProjectStatusChoices(models.TextChoices):
        CONCLUDED = 'Concluso', 'Concluso'
        LIQUIDATED = 'Liquidato', 'Liquidato'
        ONGOING = 'In corso', 'In corso'
        NOT_STARTED = 'Non avviato', 'Non avviato'
        NOT_APPLICABLE = 'Non applicabile', 'Non applicabile'

    # Enum procedural status
    class ProceduralStatusChoices(models.TextChoices):
        NOT_STARTED = 'Non avviato', 'Non avviato'
        STARTING_DESIGN = 'In avvio di progettazione', 'In avvio di progettazione'
        IN_DESIGN = 'In corso di progettazione', 'In corso di progettazione'
        IN_TENDER = 'In affidamento', 'In affidamento'
        IN_EXECUTION = 'In esecuzione', 'In esecuzione'
        EXECUTED = 'Eseguito', 'Eseguito'

    # Enum for CUP typology
    class CUPTypologyChoices(models.TextChoices):
        PURCHASE_FIXED_ASSETS = 'ACQUISTO DI IMMOBILIZZAZIONI', 'Acquisto di immobilizzazioni'
        PURCHASE_REAL_SERVICES = 'ACQUISTO SERVIZI REALI (INCLUDE FORMAZIONE)', 'Acquisto servizi reali (include formazione)'
        PURCHASE_REAL_SERVICES2 = 'ACQUISTO SERVIZI REALI (INCLUSA FORMAZIONE)', 'Acquisto servizi reali (inclusa formazione)'
        OTHER = 'ALTRO', 'Altro'
        MODERNIZATION = 'AMMODERNAMENTO', 'Ammodernamento'
        TECHNOLOGICAL_LABORATORY_MODERNIZATION = 'AMMODERNAMENTO TECNOLOGICO E LABORATORIALE', 'Ammodernamento tecnologico e laboratoriale'
        EXPANSION = 'AMPLIAMENTO', 'Ampliamento'
        WEB_APPS_PLATFORMS = 'APPLICATIVI E PIATTAFORME WEB', 'Applicativi e piattaforme web'
        ASSISTANCE = 'ASSISTENZA', 'Assistenza'
        RESEARCH_ACTIVITY = "ATTIVITA' DI RICERCA", "Attività di ricerca"
        CONSULTANCY = 'CONSULENZE', 'Consulenze'
        TRAINING_COURSES = 'CORSI DI FORMAZIONE', 'Corsi di formazione'
        FUND_ESTABLISHMENT = 'COSTITUZIONE O INCREMENTO DI FONDO PER PRESTITO', 'Costituzione o incremento di fondo per prestito'
        WORK_INCENTIVES = 'INCENTIVI AL LAVORO', 'Incentivi al lavoro'
        SOCIAL_WORKS = 'LAVORI SOCIALMENTE UTILI', 'Lavori socialmente utili'
        ORDINARY_MAINTENANCE = 'MANUTENZIONE ORDINARIA', 'Manutenzione ordinaria'
        EXTRAORDINARY_MAINTENANCE = 'MANUTENZIONE STRAORDINARIA', 'Manutenzione straordinaria'
        EXTRAORDINARY_MAINTENANCE_ENERGY = 'MANUTENZIONE STRAORDINARIA CON EFFICIENTAMENTO ENERGETICO', 'Manutenzione straordinaria con efficientamento energetico'
        EXTRAORDINARY_MAINTENANCE_ANTIFIRE = 'MANUTENZIONE STRAORDINARIA DI ADEGUAMENTO IMPIANTISTICA E O ANTINCENDIO', 'Manutenzione straordinaria adeguamento impiantistica e/o antincendio'
        EXTRAORDINARY_MAINTENANCE_SEISMIC = 'MANUTENZIONE STRAORDINARIA DI ADEGUAMENTO SISMICO', 'Manutenzione straordinaria adeguamento sismico'
        EXTRAORDINARY_MAINTENANCE_SEISMIC_IMPROV = 'MANUTENZIONE STRAORDINARIA DI MIGLIORAMENTO SISMICO', 'Manutenzione straordinaria miglioramento sismico'
        EXTRAORDINARY_MAINTENANCE_ACCESSIBILITY = "MANUTENZIONE STRAORDINARIA PER ACCESSIBILITA' E ABBATTIMENTO DELLE BARRIERE ARCHITETTONICHE", "Manutenzione straordinaria per accessibilità e abbattimento delle barriere architettoniche"
        EXTRAORDINARY_MAINTENANCE_SAFETY = 'MANUTENZIONE STRAORDINARIA PER MESSA IN SICUREZZA (ESCLUSO DISSESTO IDROGEOLOGICO)', 'Manutenzione straordinaria per messa in sicurezza (escluso dissesto idrogeologico)'
        NEW_SUPPLY = 'NUOVA FORNITURA', 'Nuova fornitura'
        NEW_REALIZATION = 'NUOVA REALIZZAZIONE', 'Nuova realizzazione'
        NEW_REALIZATION_ENERGY = 'NUOVA REALIZZAZIONE CON EFFICIENTAMENTO ENERGETICO', 'Nuova realizzazione con efficientamento energetico'
        RESEARCH_PROJECTS = 'PROGETTI DI RICERCA', 'Progetti di ricerca'
        RECOVERY = 'RECUPERO', 'Recupero'
        RESTORATION = 'RESTAURO', 'Restauro'
        RECONVERSION = 'RICONVERSIONE', 'Riconversione'
        RESTRUCTURING = "RISTRUTTURAZIONE (PER CAMBIO DI DESTINAZIONE D'USO)", "Ristrutturazione (per cambio di destinazione d'uso)"
        RESTRUCTURING_ENERGY = 'RISTRUTTURAZIONE CON EFFICIENTAMENTO ENERGETICO', 'Ristrutturazione con efficientamento energetico'
        INCOME_SUPPORT = 'SOSTEGNO AL REDDITO CON RISORSE FSC E/O SIE', 'Sostegno al reddito con risorse FSC e/o SIE'
        STUDIES_DESIGNS = 'STUDI E PROGETTAZIONI', 'Studi e progettazioni'
        STUDIES_TERRITORIAL_PLANNING = 'STUDI E PROGETTAZIONI O PIANIFICAZIONE TERRITORIALE', 'Studi e progettazioni o pianificazione territoriale'
        STUDIES_DESIGNS_ENERGY = 'STUDI E PROGETTAZIONI PER EFFICIENTAMENTO ENERGETICO', 'Studi e progettazioni per efficientamento energetico'
        TRANSFER = 'TRASFERIMENTO', 'Trasferimento'
        DEMOLITION = 'DEMOLIZIONE', 'Demolizione'
        PURCHASE_FIXED_ASSETS_FISHING_COMPANIES = 'ACQUISTO DI IMMOBILIZZAZIONI (AD ESEMPIO PESCHERECCI O AZIENDE)', 'Acquisto di immobilizzazioni (ad esempio pescherecci o aziende)'
        MODERNIZATION_WITH_ENERGY_EFFICIENCY = 'AMMODERNAMENTO CON EFFICIENTAMENTO ENERGETICO', 'Ammodernamento con efficientamento energetico'
        EXPANSION_OR_STRENGTHENING = 'AMPLIAMENTO (COMPRESA SOPRAELEVAZIONE) O POTENZIAMENTO', 'Ampliamento (compresa sopraelevazione) o potenziamento'
        EXPANSION_WITH_ENERGY_EFFICIENCY = 'AMPLIAMENTO CON EFFICIENTAMENTO ENERGETICO', 'Ampliamento con efficientamento energetico'
        PATENTS = 'BREVETTI', 'Brevetti'
        FUND_ESTABLISHMENT_GUARANTEE = 'COSTITUZIONE O INCREMENTO DI FONDO PER GARANZIA', 'Costituzione o incremento di fondo per garanzia'
        MAINTENANCE_WITH_ENERGY_EFFICIENCY = 'MANUTENZIONE CON EFFICIENTAMENTO ENERGETICO', 'Manutenzione con efficientamento energetico'
        EXTRAORDINARY_MAINTENANCE_HYDROGEOLOGICAL = 'MANUTENZIONE STRAORDINARIA PER DISSESTO IDROGEOLOGICO', 'Manutenzione straordinaria per dissesto idrogeologico'
        RESTRUCTURING_SIMPLE = 'RISTRUTTURAZIONE', 'Ristrutturazione'
        STUDIES_DESIGNS_FOR_ACCESSIBILITY = 'STUDI E PROGETTAZIONI PER ABBATTIMENTO BARRIERE ARCHITETTONICHE', 'Studi e progettazioni per abbattimento barriere architettoniche'
        STUDIES_DESIGNS_TECH_LAB_MODERNIZATION = 'STUDI E PROGETTAZIONI PER AMMODERNAMENTO TECNOLOGICO E LABORATORIALE', 'Studi e progettazioni per ammodernamento tecnologico e laboratoriale'
        STUDIES_DESIGNS_HYDROGEOLOGICAL = 'STUDI E PROGETTAZIONI PER DISSESTO IDROGEOLOGICO', 'Studi e progettazioni per dissesto idrogeologico'
        STUDIES_DESIGNS_SEISMIC_IMPROVEMENT = 'STUDI E PROGETTAZIONI PER IL MIGLIORAMENTO SISMICO', 'Studi e progettazioni per il miglioramento sismico'
        STUDIES_DESIGNS_SEISMIC_ADAPTATION = 'STUDI E PROGETTAZIONI PER L\'ADEGUAMENTO SISMICO', 'Studi e progettazioni per l\'adeguamento sismico'
        STUDIES_DESIGNS_FOR_SAFETY_EXCLUDING_HYDRO = 'STUDI E PROGETTAZIONI PER MESSA IN SICUREZZA (ESCLUSO DISSESTO IDROGEOLOGICO)', 'Studi e progettazioni per messa in sicurezza (escluso dissesto idrogeologico)'
        STUDIES_DESIGNS_NEW_REALIZATION = 'STUDI E PROGETTAZIONI PER NUOVA REALIZZAZIONE', 'Studi e progettazioni per nuova realizzazione'
        STUDIES_DESIGNS_RECOVERY = 'STUDI E PROGETTAZIONI PER RECUPERO', 'Studi e progettazioni per recupero'

    # Attributes
    local_project_code = models.CharField(max_length=100, primary_key=True)  # COD_LOCALE_PROGETTO
    oc_project_status = models.CharField(
        max_length=100,
        choices=ProjectStatusChoices.choices,
        default=ProjectStatusChoices.NOT_APPLICABLE
    )  # OC_STATO_PROGETTO
    oc_procedural_state = models.CharField(
        max_length=100,
        choices=ProceduralStatusChoices.choices,
        default=ProceduralStatusChoices.NOT_STARTED
    )  # OC_STATO_PROCEDURALE
    cup_typology = models.CharField(
        max_length=255,
        choices=CUPTypologyChoices.choices,
        blank=True,
        null=True
    )  # CUP_DESCR_TIPOLOGIA
    oc_project_title = models.TextField()  # OC_TITOLO_PROGETTO
    cup_descr_sector = models.CharField(max_length=255, blank=True, null=True)  # CUP_DESCR_SETTORE
    oc_synthetic_theme = models.CharField(max_length=255, blank=True, null=True)  # OC_TEMA_SINTETICO

class Funding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="funding")

    # Public funds
    eu_funds = models.FloatField(default=0)  # FINANZ_UE
    eu_funds_fesr = models.FloatField(default=0)  # FINANZ_UE_FESR
    eu_funds_fse = models.FloatField(default=0)  # FINANZ_UE_FSE
    eu_funds_feasr = models.FloatField(default=0)  # FINANZ_UE_FEASR
    eu_funds_feamp = models.FloatField(default=0)  # FINANZ_UE_FEAMP
    eu_funds_iog = models.FloatField(default=0)  # FINANZ_UE_IOG
    state_rotating_fund = models.FloatField(default=0)  # FINANZ_STATO_FONDO_DI_ROTAZIONE
    state_fsc = models.FloatField(default=0)  # FINANZ_STATO_FSC
    state_pac = models.FloatField(default=0)  # FINANZ_STATO_PAC
    state_completions = models.FloatField(default=0)  # FINANZ_STATO_COMPLETAMENTI
    state_other_measures = models.FloatField(default=0)  # FINANZ_STATO_ALTRI_PROVVEDIMENTI
    regional_funds = models.FloatField(default=0)  # FINANZ_REGIONE
    provincial_funds = models.FloatField(default=0)  # FINANZ_PROVINCIA
    municipal_funds = models.FloatField(default=0)  # FINANZ_COMUNE
    freed_resources = models.FloatField(default=0)  # FINANZ_RISORSE_LIBERATE
    other_public_funds = models.FloatField(default=0)  # FINANZ_ALTRO_PUBBLICO

    # Extra funds
    foreign_state = models.FloatField(default=0)  # FINANZ_STATO_ESTERO
    private_funds = models.FloatField(default=0)  # FINANZ_PRIVATO
    funds_to_find = models.FloatField(default=0)  # FINANZ_DA_REPERIRE

    # Economies
    total_savings = models.FloatField(default=0)  # ECONOMIE_TOTALI
    total_public_savings = models.FloatField(default=0)  # ECONOMIE_TOTALI_PUBBLICHE

    # Calculated totals
    total_funds_gross = models.FloatField(blank=True, null=True)  # Gross
    total_funds_net = models.FloatField(blank=True, null=True)  # Net

    def save(self, *args, **kwargs):
        # Gross total = sum of all funds
        self.total_funds_gross = (
                self.eu_funds + self.eu_funds_fesr + self.eu_funds_fse + self.eu_funds_feasr + self.eu_funds_feamp +
                self.eu_funds_iog + self.state_rotating_fund + self.state_fsc + self.state_pac + self.state_completions
                + self.state_other_measures + self.regional_funds + self.provincial_funds + self.municipal_funds +
                self.freed_resources + self.other_public_funds + self.foreign_state + self.private_funds +
                self.funds_to_find
        )

        # Net total = gross - total savings
        self.total_funds_net = self.total_funds_gross - (self.total_savings or 0)

        super().save(*args, **kwargs)

class Location(models.Model):

    # 1. Definition of enum of 'macroarea'
    class MacroAreaChoices(models.TextChoices):
        OTHER = 'Altro', 'Altro'
        NATIONAL_SCOPE = 'Ambito Nazionale', 'Ambito Nazionale'
        MIDDLE_NORTH = 'Centro-Nord', 'Centro-Nord'
        ABROAD = 'Estero', 'Estero'
        MIDDAY = 'Mezzogiorno', 'Mezzogiorno'
        TRASVERSAL = 'Traversale', 'Trasversale'
    region_code = models.CharField(max_length=20, primary_key = True)
    region_name = models.CharField(max_length=50)
    macroarea = models.CharField(
        max_length=50,
        choices=MacroAreaChoices.choices,
        default=MacroAreaChoices.OTHER,
        verbose_name='Macro Area'
    )
    project = models.ManyToManyField('Project', related_name='locations')