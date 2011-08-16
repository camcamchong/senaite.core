from AccessControl import ClassSecurityInfo
from Products.ATExtensions.ateapi import RecordsField
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.fields import DurationField
from bika.lims.browser.widgets import ServicesWidget, RecordsWidget, \
     DurationWidget
from bika.lims.config import ATTACHMENT_OPTIONS, I18N_DOMAIN, PROJECTNAME, \
    POINTS_OF_CAPTURE
from bika.lims.content.bikaschema import BikaSchema
from zope.interface import implements
import sys

schema = BikaSchema.copy() + Schema((
    BooleanField('ReportDryMatter',
        default = False,
        widget = BooleanWidget(
            label = "Report as dry matter",
            label_msgid = "label_report_dry_matter",
            description = "Select if result can be reported as dry matter",
            description_msgid = 'help_report_dry_matter',
        ),
    ),
    StringField('AttachmentOption',
        default = 'p',
        vocabulary = ATTACHMENT_OPTIONS,
        widget = SelectionWidget(
            label = 'Attachment option',
            label_msgid = 'label_attachment_option',
        ),
    ),
    StringField('Unit',
        index = "FieldIndex:brains",
        widget = StringWidget(
            label_msgid = 'label_unit',
        ),
    ),
    IntegerField('Precision',
        widget = IntegerWidget(
            label = "Precision as number of decimals",
            label_msgid = 'label_precision',
            description = 'Define the number of decimals to be used for this result',
            description_msgid = 'help_precision',
        ),
    ),
    FixedPointField('Price',
        index = "FieldIndex:brains",
        default = '0.00',
        widget = DecimalWidget(
            label = 'Price excluding VAT',
            label_msgid = 'label_price_excl_vat',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    FixedPointField('CorporatePrice',
        default = '0.00',
        widget = DecimalWidget(
            label = 'Corporate price excluding VAT',
            label_msgid = 'label_corporate_price_excl_vat',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    ComputedField('VATAmount',
        expression = 'context.getVATAmount()',
        widget = ComputedWidget(
            label = 'VAT',
            label_msgid = 'label_vat',
            i18n_domain = I18N_DOMAIN,
            visible = {'edit':'hidden', }
        ),
    ),
    ComputedField('TotalPrice',
        expression = 'context.getTotalPrice()',
        widget = ComputedWidget(
            label = 'Total price',
            label_msgid = 'label_totalprice',
            i18n_domain = I18N_DOMAIN,
            visible = {'edit':'hidden', }
        ),
    ),
    FixedPointField('VAT',
        index = 'FieldIndex:brains',
        default_method = 'getDefaultVAT',
        widget = DecimalWidget(
            label = 'VAT %',
            label_msgid = 'label_vat_percentage',
            description = 'Enter percentage value eg. 14',
            description_msgid = 'help_vat_percentage',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    StringField('Keyword',
        required = 1,
        index = 'FieldIndex:brains',
        validators = ('isUnixLikeName','ServiceKeywordValidator'),
        widget = StringWidget(
            label = 'Analysis Keyword',
            label_msgid = 'label_analysis_keyword',
            description = 'This is the name of the service in instrument exports and AR imports.  It is also the service identifier used in user defined calculations.',
        ),
    ),
    ReferenceField('Instrument',
        required = 0,
        vocabulary_display_path_bound = sys.maxint,
        allowed_types = ('Instrument',),
        relationship = 'AnalysisServiceInstrument',
        referenceClass = HoldingReference,
        widget = ReferenceWidget(
            checkbox_bound = 1,
            label = 'Instrument',
            label_msgid = 'label_instrument',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    ReferenceField('Calculation',
        required = 0,
        vocabulary_display_path_bound = sys.maxint,
        allowed_types = ('Calculation',),
        relationship = 'AnalysisServiceCalculation',
        referenceClass = HoldingReference,
        widget = ReferenceWidget(
            checkbox_bound = 1,
            label = 'Calculation',
            label_msgid = 'label_calculation',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    DurationField('MaxTimeAllowed',
        widget = DurationWidget(
            label = "Maximum time allowed",
            description = 'Maximum time allowed for ' \
                        'publication of results',
            description_msgid = 'help_max_hours_allowed',
        ),
    ),
    FixedPointField('DuplicateVariation',
        widget = DecimalWidget(
            label = 'Duplicate Variation',
            label_msgid = 'label_duplicate_variation',
            description = 'Enter duplicate variation permitted as percentage',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    BooleanField('Accredited',
        index = "FieldIndex:brains",
        default = False,
        widget = BooleanWidget(
            label = "Accredited",
            label_msgid = "label_accredited"
        ),
    ),
    StringField('PointOfCapture',
        required = 1,
        index = "FieldIndex:brains",
        default = 'lab',
        vocabulary = POINTS_OF_CAPTURE,
        widget = SelectionWidget(
            format = 'flex',
            label = 'Analysis Point of Capture',
            label_msgid = 'label_pointofcapture',
            description = "This decides when analyses are performed.  A sample's field analyses results are entered when an analysis request is created, and lab analyses are captured into existing ARs.",
        ),
    ),
    ReferenceField('Category',
        required = 1,
        vocabulary_display_path_bound = sys.maxint,
        allowed_types = ('AnalysisCategory',),
        relationship = 'AnalysisServiceAnalysisCategory',
        referenceClass = HoldingReference,
        widget = ReferenceWidget(
            checkbox_bound = 1,
            label = 'Analysis category',
            label_msgid = 'label_category',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    ReferenceField('Department',
        required = 0,
        vocabulary_display_path_bound = sys.maxint,
        allowed_types = ('Department',),
        relationship = 'AnalysisServiceDepartment',
        referenceClass = HoldingReference,
        widget = ReferenceWidget(
            checkbox_bound = 1,
            label = 'Department',
            label_msgid = 'label_department',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    ComputedField('CategoryName',
        index = 'FieldIndex',
        expression = "context.getCategory() and context.getCategory().Title() or ''",
        widget = ComputedWidget(
            label = "Analysis category",
            visible = {'edit':'hidden', }
        ),
    ),
    ComputedField('CategoryUID',
        index = 'FieldIndex',
        expression = "context.getCategory() and context.getCategory().UID() or ''",
        widget = ComputedWidget(
            label = "Analysis category",
            visible = {'edit':'hidden', }
        ),
    ),
    RecordsField('Uncertainties',
        type = 'uncertainties',
        subfields = ('intercept_min', 'intercept_max', 'errorvalue'),
        required_subfields = ('intercept_min', 'intercept_max', 'errorvalue'),
        subfield_sizes = {'intercept_min': 10,
                           'intercept_max': 10,
                           'errorvalue': 10,
                           },
        subfield_labels = {'intercept_min': 'Min',
                           'intercept_max': 'Max',
                           'errorvalue': 'Actual value',
                           },
        widget = RecordsWidget(
            label = 'Uncertainties',
            label_msgid = 'label_uncertainties',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    RecordsField('ResultOptions',
        type = 'resultsoptions',
        subfields = ('Result',),
        required_subfields = ('Result',),
        subfield_labels = {'Result': 'Option Text',},
        widget = RecordsWidget(
            label = 'Result Options',
            label_msgid = 'label_result_options',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
))

schema['id'].widget.visible = False

class AnalysisService(BaseContent):
    security = ClassSecurityInfo()
    schema = schema

    security.declarePublic('getDiscountedPrice')
    def getDiscountedPrice(self):
        """ compute discounted price excl. vat """
        price = self.getPrice()
        price = price and price or 0
        discount = self.bika_setup.getMemberDiscount()
        discount = discount and discount or 0
        return float(price) - (float(price) * float(discount)) / 100

    security.declarePublic('getDiscountedCorporatePrice')
    def getDiscountedCorporatePrice(self):
        """ compute discounted corporate price excl. vat """
        price = self.getCorporatePrice()
        price = price and price or 0
        discount = self.bika_setup.getMemberDiscount()
        discount = discount and discount or 0
        return float(price) - (float(price) * float(discount)) / 100

    def getTotalPrice(self):
        """ compute total price """
        price = self.getPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    def getTotalCorporatePrice(self):
        """ compute total price """
        price = self.getCorporatePrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    security.declarePublic('getTotalDiscountedPrice')
    def getTotalDiscountedPrice(self):
        """ compute total discounted price """
        price = self.getDiscountedPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    security.declarePublic('getTotalDiscountedCorporatePrice')
    def getTotalDiscountedCorporatePrice(self):
        """ compute total discounted corporate price """
        price = self.getDiscountedCorporatePrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    def getDefaultVAT(self):
        """ return default VAT from bika_setup """
        try:
            vat = self.bika_setup.getVAT()
            return vat
        except ValueError:
            return "0.00"

    security.declarePublic('getVATAmount')
    def getVATAmount(self):
        """ Compute VATAmount
        """
        try:
            return "%.2f" % (self.getTotalPrice() - self.getPrice())
        except:
            return "0.00"

    def getUncertainty(self, result=None):
        """ Return the uncertainty value, if the result falls within specified ranges for this
            service. """
        if result is None:
            return None

        uncertainties = self.getUncertainties()
        if uncertainties:
            try:
                result = float(result)
            except:
                # if it's not a number, we assume no measure of uncertainty
                return None

            for d in uncertainties:
                if float(d['intercept_min']) <= result < float(d['intercept_max']):
                    return d['errorvalue']
            return None
        else:
            return None

    def duplicateService(self, context):
        """ Create a copy of the service and return the copy's id """
        dup_id = context.generateUniqueId(type_name = 'AnalysisService')
        context.invokeFactory(id = dup_id, type_name = 'AnalysisService')
        dup = context[dup_id]
        dup.setTitle('! Copy of %s' % self.Title())
        dup.edit(
            description = self.Description(),
            Instructions = self.getInstructions(),
            ReportDryMatter = self.getReportDryMatter(),
            Unit = self.getUnit(),
            Precision = self.getPrecision(),
            Price = self.getPrice(),
            CorporatePrice = self.getCorporatePrice(),
            VAT = self.getVAT(),
            Keyword = self.getKeyword(),
            Instrument = self.getInstrument(),
            Calculation = self.getCalculation(),
            MaxTimeAllowed = self.getMaxTimeAllowed(),
            TitrationUnit = self.getTitrationUnit(),
            DuplicateVariation = self.getDuplicateVariation(),
            AnalysisCategory = self.getAnalysisCategory(),
            Department = self.getDepartment(),
            Accredited = self.getAccredited(),
            Uncertainties = self.getUncertainties(),
            ResultOptions = self.getResultOptions(),
            )
        dup.reindexObject()
        return dup_id

registerType(AnalysisService, PROJECTNAME)
