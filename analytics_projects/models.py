from django.db import models

#Classe del progetto

class Funding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

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
        OTHER = 'ALTRO', 'ALTRO'
        NATIONAL SCOPE = 'AMBITO NAZIONALE', 'AMBITO NAZIONALE'
        MIDDLE-NORTH = 'CENTRO-NORD', 'CENTRO-NORD'
        ABROAD = 'ESTERO', 'ESTERO'
        MIDDAY = 'MEZZOGIORNO', 'MEZZOGIORNO'
        TRASVERSAL = 'TRASVERSALE', 'TRASVERSALE'

    common_code = models.CharField(max_length=9)
    common_name = models.CharField(max_length=35)
    province_code = models.CharField(max_length=6)
    province_name = models.CharField(max_length=21)
    region_code = models.CharField(max_length=3)
    region_name = models.CharField(max_length=20)  
    macroarea = models.CharField(
        max_length=15,  
        choices=MacroAreaChoices.choices,
        default=MacroAreaChoices.OTHER,
        verbose_name='Macro Area'
    )
    project = models.ManyToManyField('Project', related_name='locations')