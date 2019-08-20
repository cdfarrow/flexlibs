#
#   FLExProject.py
#
#   Class: FLExProject
#            Fieldworks Language Explorer project access functions 
#            via SIL Language and Culture Model (LCM) API.
#
#
#   Platform: Python.NET
#             (ITsString doesn't work in IRONPython)
#             FieldWorks Version 9
#
#   Copyright Craig Farrow, 2008 - 2019
#
from __future__ import print_function
from __future__ import absolute_import

from builtins import str
from builtins import object

# Initialise low-level FLEx data access
from . import FLExInit
from . import FLExLCM

import clr
clr.AddReference("System")
import System

from SIL.LCModel import (
    ICmObjectRepository,
    ILexEntryRepository, ILexEntry, LexEntryTags,
                         ILexSense, LexSenseTags,
    IWfiWordformRepository, WfiWordformTags,
                            WfiGlossTags,
    IWfiAnalysisRepository, IWfiAnalysis, WfiAnalysisTags,
                            WfiMorphBundleTags,
    ITextRepository,
    ISegmentRepository,
    IReversalIndex, IReversalIndexEntry, ReversalIndexEntryTags,
    IMoMorphType,
    SpecialWritingSystemCodes,
    IMultiStringAccessor,
    LcmInvalidFieldException,
    IUndoStackManager,
    )


from SIL.LCModel.Core.Cellar import CellarPropertyType
from SIL.LCModel.Core.KernelInterfaces import ITsString, ITsStrBldr
from SIL.LCModel.Core.Text import TsStringUtils
import SIL.FieldWorks.Common.FwUtils


#--- Exceptions ------------------------------------------------------

class FP_ProjectError(Exception):
    """Exception raised for any problems opening the project.

    Attributes:
        - message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class FP_FileNotFoundError(FP_ProjectError):
    def __init__(self, projectName):
        FP_ProjectError.__init__(self,
            "Project file not found: %s" % projectName)

class FP_FileLockedError(FP_ProjectError):
    def __init__(self):
        FP_ProjectError.__init__(self,
            "This project is in use by another program. Please close the other program and try again.")
            
class FP_MigrationRequired(FP_ProjectError):
    def __init__(self):
        FP_ProjectError.__init__(self,
            "This project needs to be opened in FieldWorks in order for it to be migrated to the latest format.")

#-----------------------------------------------------            

class FP_RuntimeError(Exception):
    """Exception raised for any problems running the module.

    Attributes:
        - message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class FP_ReadOnlyError(FP_RuntimeError):
    def __init__(self):
        FP_RuntimeError.__init__(self,
            "Trying to write to the project database without changes enabled.")
            
class FP_WritingSystemError(FP_RuntimeError):
    def __init__(self, writingSystemName):
        FP_RuntimeError.__init__(self,
            "Invalid Writing System for this project: %s" % writingSystemName)

class FP_NullParameterError(FP_RuntimeError):
    def __init__(self):
        FP_RuntimeError.__init__(self,
            "Null parameter.")

class FP_ParameterError(FP_RuntimeError):
    def __init__(self, msg):
        FP_RuntimeError.__init__(self, msg)
        
#-----------------------------------------------------------
def GetProjectNames():
    """
    Returns a list of FieldWorks projects that are in the default location.
    """
    
    return FLExLCM.GetListOfProjects()

#-----------------------------------------------------------
   
class FLExProject (object):
    """
    This class provides convenience methods for accessing a FieldWorks 
    project by hiding some of the complexity of LCM.
    For functionality that isn't provided here, LCM data and methods
    can be used directly via FLExProject.project, FLExProject.lp and
    FLExProject.lexDB; 
    However, for long term use, new methods should be added to this class.

    Usage::

        fp = FLExProject()
        try:
            fp.OpenProject("my project",
                           writeEnabled = True/False)
        except:
            #"Failed to open project"
            del fp

    """
        
    def OpenProject(self, 
                    projectName, 
                    writeEnabled = False):
        """
        Open a project.

        projectName:
            - Either the full path including ".fwdata" suffix, or
            - The name only, to open from the default project location.
            
        writeEnabled: 
            configures FW to accept database changes, and
            saves those when this object is deleted. It will also be used to
            open the FW project in read-only mode so that FW doesn't have to
            be closed for read-only operations. (Awaiting support in a future
            release of FW)

        """
        
        try:
            self.project = FLExLCM.OpenProject(projectName, 
                                               writeEnabled)
            
        except System.IO.FileNotFoundException as e:
            raise FP_FileNotFoundError(projectName)
            
        except SIL.LCModel.LcmFileLockedException as e:
            raise FP_FileLockedError()
        
        except (SIL.LCModel.LcmDataMigrationForbiddenException,           
                SIL.LCModel.Utils.WorkerThreadException) as e:
            # Raised if the FW project needs to be migrated
            # to a later version. The user needs to open the project 
            # in FW to do the migration.
            raise FP_MigrationRequired()
            
        except SIL.FieldWorks.Common.FwUtils.StartupException as e:
            # An unknown error -- pass on the full information
            raise FP_ProjectError(e.Message)


        self.lp    = self.project.LangProject
        self.lexDB = self.lp.LexDbOA
        
        # Set up FieldWorks for making changes to the project.
        # All changes will be automatically saved when this object is
        # deleted.

        self.writeEnabled = writeEnabled
        
        if self.writeEnabled:
            try:
                # This must be called before calling any methods that change
                # the project.
                self.project.MainCacheAccessor.BeginNonUndoableTask()
            except System.InvalidOperationException:
                raise FP_ProjectError("BeginNonUndoableTask() failed.")

    def ProjectName(self):
        """
        Returns the display name of the current project.
        """

        return self.project.ProjectId.UiName
            
    def __del__(self):
        if hasattr(self, "project"):
            if self.writeEnabled:
                # This must be called to mirror the call to BeginNonUndoableTask().
                self.project.MainCacheAccessor.EndNonUndoableTask()
                # Save all changes to disk. (EndNonUndoableTask)
                usm = self.project.ServiceLocator.GetInstance(IUndoStackManager)
                usm.Save()                
            try:
                #print "Calling self.project.Dispose()"
                # TODO: This is failing with a COM error (memory disposal problem)
                # with the Lela-Teli projects only.
                self.project.Dispose()
                del self.project
                #print "FLExProject.__del__: success"
                return
            except:
                #import traceback
                #print "FLExProject.__del__:\n %s\n" % (traceback.format_exc())
                raise
                pass
            #print "FLExProject.__del__: failed"


    # --- String Utilities ---

    def BestStr(self, stringObj):
        """
        Generic string extraction function returning the best Analysis or Vernacular string.
        """
        if not stringObj: raise FP_NullParameterError()
        
        s = ITsString(stringObj.BestAnalysisVernacularAlternative).Text
        return u"" if s == "***" else s
        
    # --- LCM Utilities ---
    
    def UnpackNestedPossibilityList(self, possibilityList, flat=False):
        """
        Returns a nested or flat list of a Fieldworks Possibility List.
        
        Return items are objects with properties/methods:
            - Hvo         - ID (value not the same across projects)
            - Guid        - Global Unique ID (same across all projects)
            - ToString()  - String representation.
        """
        for i in possibilityList:
            yield i
            if flat:
                for j in self.UnpackNestedPossibilityList(i.SubPossibilitiesOS, flat):
                    yield j
            else:
                l = list(self.UnpackNestedPossibilityList(i.SubPossibilitiesOS, flat))
                if l: yield l
    
    # --- Global: Writing Systems ---

    def GetAllVernacularWSs(self):
        """
        Returns a set of language tags for all vernacular writing systems used
        in this project.
        """
        return set(self.lp.CurVernWss.split())
           
           
    def GetAllAnalysisWSs(self):
        """
        Returns a set of language tags for all analysis writing systems used
        in this project.
        """
        return set(self.lp.CurAnalysisWss.split())

        
    def GetWritingSystems(self):
        """
        Returns the Writing Systems that are active in this project as a
        list of tuples: (Name, Language-tag, Handle, IsVernacular).
        Use the Language-tag when specifying Writing System to other
        functions.
        """

        VernWSSet = self.GetAllVernacularWSs()
        AnalWSSet = self.GetAllAnalysisWSs()
        
        WSList = []
        # The names of WS associated with this project.
        # Sorted and with no duplicates.
        for x in self.project.ServiceLocator.WritingSystems.AllWritingSystems:
            if x.Id in VernWSSet:
                isVern = True
            elif x.Id in AnalWSSet:
                isVern = False
            else:
                continue        # Skip non-active WSs
            WSList.append( (x.DisplayLabel, x.Id, x.Handle, isVern) )
        return WSList

        
    def WSUIName(self, languageTagOrHandle):
        """
        Returns the UI name of the writing system for the given languageTag or Handle.
        Ignores case and '-'/'_' differences.
        Returns None if the language tag is not found.
        """

        if isinstance(languageTagOrHandle, str):
            languageTagOrHandle = self.__NormaliseLangTag(languageTagOrHandle)
        
        try:
            return self.__WSNameCache[languageTagOrHandle]
        except AttributeError:
            # Create a lookup table on-demand.
            self.__WSNameCache = {}
            for x in self.project.ServiceLocator.WritingSystems.AllWritingSystems:
                langTag = self.__NormaliseLangTag(x.Id)
                self.__WSNameCache[langTag] = x.DisplayLabel
                self.__WSNameCache[x.Handle] = x.DisplayLabel
            # Recursive:
            return self.WSUIName(languageTagOrHandle)
        except KeyError:
            return None

            
    def WSHandle(self, languageTag):
        """
        Returns the Handle of the writing system for the given languageTag.
        Ignores case and '-'/'_' differences.
        Returns None if the language tag is not found.
        """
        
        languageTag = self.__NormaliseLangTag(languageTag)
        
        try:
            return self.__WSLCIDCache[languageTag]
        except AttributeError:
            # Create a lookup table on-demand.
            self.__WSLCIDCache = {}
            for x in self.project.ServiceLocator.WritingSystems.AllWritingSystems:
                langTag = self.__NormaliseLangTag(x.Id)
                self.__WSLCIDCache[langTag] = x.Handle
            # Recursive:
            return self.WSHandle(languageTag)
        except KeyError:
            return None
            
            
    def GetDefaultVernacularWS(self):
        """
        Returns the Default Vernacular Writing System: (Language-tag, Name)
        """
        return (self.lp.DefaultVernacularWritingSystem.Id,
                self.lp.DefaultVernacularWritingSystem.DisplayLabel)
    
    
    def GetDefaultAnalysisWS(self):
        """
        Returns the Default Analysis Writing System: (Language-tag, Name)
        """
        return (self.lp.DefaultAnalysisWritingSystem.Id,
                self.lp.DefaultAnalysisWritingSystem.DisplayLabel)

    # --- Global: other information ---
    
    def GetDateLastModified(self):
        return self.lp.DateModified
    
    
    def GetPartsOfSpeech(self):
        """
        Returns a list of the Parts of Speech defined in this project.
        """
        pos = self.lp.AllPartsOfSpeech
        
        return [x.ToString() for x in pos]

        
    def GetAllSemanticDomains(self, flat=False):
        """
        Returns a nested or flat list of all Semantic Domains defined
        in this project. The list is ordered.
        
        Return items are objects with properties/methods:

            - Hvo         - ID (value not the same across projects)
            - Guid        - Global Unique ID (same across all projects)
            - ToString()  - String representation of the semantic domain.
        """

        # Recursively extract the semantic domains
        return list(self.UnpackNestedPossibilityList(
                        self.lp.SemanticDomainListOA.PossibilitiesOS,
                        flat))


    # --- Global utility functions ---
    
    def BuildGotoURL(self, objectOrGuid):
        """
        Builds a URL that can be used with os.startfile() to jump to the
        object in Fieldworks. This method currently supports:

            - Lexical Entries
            - Reversal Entries
            - Wordforms
        """

        if isinstance(objectOrGuid, System.Guid):
            guidString = str(objectOrGuid)
            objRepository = self.project.ServiceLocator.GetInstance(ICmObjectRepository)
            object = objRepository.GetObject(objectOrGuid)

        else:
             try:
                guidString = str(objectOrGuid.Guid)
                object = objectOrGuid
             except:
                raise FP_ParameterError("BuildGotoURL: objectOrGuid is neither System.Guid or an object with attribute Guid")

        if object.ClassID == ReversalIndexEntryTags.kClassId:
            tool = u"reversalToolEditComplete"

        elif object.ClassID in (WfiWordformTags.kClassId,
                                WfiAnalysisTags.kClassId,
                                WfiGlossTags.kClassId):
            tool = u"Analyses"

        else:
            tool = u"lexiconEdit"                # Default tool is Lexicon Edit

        return r"%26".join([r"silfw://localhost/link?app%3dflex",
                            r"database%3d" + self.project.ProjectId.UiName.replace(" ", "+"),
                            r"tool%3d" + tool,
                            r"guid%3d" + guidString,])


    # --- Generic Repository Access ---

    def ObjectCountFor(self, repository):
        """
        Returns the number of objects in the given repository.
        repository is specified by the interface class, such as:
        
            - ITextRepository
            - ILexEntryRepository

        (All repository names can be viewed by opening a project in
        LCMBrowser, which can be launched via the Help menu.)
        """
        
        repo = self.project.ServiceLocator.GetInstance(repository)
        return repo.Count
    
    
    def ObjectsIn(self, repository):
        """
        Returns an iterator over all the objects in the given repository.
        repository is specified by the interface class, such as:
        
            - ITextRepository
            - ILexEntryRepository
            
        Open a project in LCMBrowser to identify other repository names.
        """

        repo = self.project.ServiceLocator.GetInstance(repository)
        return iter(repo.AllInstances())
        
    # --- Lexicon ---

    def LexiconNumberOfEntries(self):
        return self.ObjectCountFor(ILexEntryRepository)
        
    def LexiconAllEntries(self):
        """
        Returns an iterator over all entries in the lexicon.
        
        Each entry is of type::

          SIL.LCModel.ILexEntry, which contains:
              - HomographNumber :: integer
              - HomographForm :: string
              - LexemeFormOA ::  SIL.LCModel.Ling.MoForm
                   - Form :: SIL.LCModel.MultiUnicodeAccessor
                      - GetAlternative : Get String for given WS type
                      - SetAlternative : Set string for given WS type
              - SensesOS :: Ordered collection of SIL.LCModel.Ling.LexSense 
                  - Gloss :: SIL.LCModel.MultiUnicodeAccessor
                  - Definition :: SIL.LCModel.MultiStringAccessor
                  - SenseNumber :: string
                  - ExamplesOS :: Ordered collection of LexExampleSentence
                      - Example :: MultiStringAccessor
        """
        
        return self.ObjectsIn(ILexEntryRepository)


    #  (Writing system utilities)
    
    def __WSHandle(self, languageTagOrHandle, defaultWS):
        if languageTagOrHandle == None:
            handle = defaultWS
        else:
            #print "Specified ws =", languageTagOrHandle
            if isinstance(languageTagOrHandle, str):
                handle = self.WSHandle(languageTagOrHandle)
            else:
                handle = languageTagOrHandle
        if not handle:
            raise FP_WritingSystemError(languageTagOrHandle)
        return handle

    def __WSHandleVernacular(self, languageTagOrHandle):
        return self.__WSHandle(languageTagOrHandle,
                               self.project.DefaultVernWs)

    def __WSHandleAnalysis(self, languageTagOrHandle):
        return self.__WSHandle(languageTagOrHandle,
                               self.project.DefaultAnalWs)
    
    def __NormaliseLangTag(self, languageTag):
        return languageTag.replace("-", "_").lower()
    
    #  (Vernacular WS fields)
    
    def LexiconGetHeadword(self, entry):
        """
        Returns the headword for the entry
        """
        return entry.ReferenceName

        
    def LexiconGetLexemeForm(self, entry, languageTagOrHandle=None):
        """
        Returns the lexeme form for the entry in the Default Vernacular WS
        or other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleVernacular(languageTagOrHandle)

        # MultiUnicodeAccessor
        form = ITsString(entry.LexemeFormOA.Form.get_String(WSHandle)).Text
        return form or u""

        
    def LexiconGetCitationForm(self, entry, languageTagOrHandle=None):
        """
        Returns the citation form for the entry in the Default Vernacular WS
        or other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleVernacular(languageTagOrHandle)

        # MultiUnicodeAccessor
        form = ITsString(entry.CitationForm.get_String(WSHandle)).Text
        return form or u""

        
    def LexiconGetPublishInCount(self, entry):
        """
        Returns the PublishIn Count
        """
        return entry.PublishIn.Count

        
    def LexiconGetPronunciation(self, pronunciation, languageTagOrHandle=None):
        """
        Returns the Form for the Pronunciation in the Default Vernacular WS
        or other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleVernacular(languageTagOrHandle)

        # MultiUnicodeAccessor
        form = ITsString(pronunciation.Form.get_String(WSHandle)).Text
        return form or u""

        
    def LexiconGetExample(self, example, languageTagOrHandle=None):
        """
        Returns the example text in the Default Vernacular WS or
        other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleVernacular(languageTagOrHandle)
        
        # Example is a MultiString
        ex = ITsString(example.Example.get_String(WSHandle)).Text
        return ex or u""

        
    def LexiconSetExample(self, example, newString, languageTagOrHandle=None):
        """
        Set the Default Vernacular string for the given Example:
        
            - newString must be unicode.
            - languageTagOrHandle specifies a different writing system.

        NOTE: using this function will lose any formatting that might
        have been present in the example string.
        """

        if not self.writeEnabled: raise FP_ReadOnlyError
        
        if not example: raise FP_NullParameterError()

        WSHandle = self.__WSHandleVernacular(languageTagOrHandle)

        # Example is a MultiString
        example.Example.set_String(WSHandle, newString)
        return

        
    def LexiconGetExampleTranslation(self, translation, languageTagOrHandle=None):
        """
        Returns the translation of an example in the Default Analysis WS or
        other WS as specified by languageTagOrHandle.

        NOTE: Analysis language translations of example sentences are
        stored as a collection (list). E.g.::

            for translation in example.TranslationsOC:
                print (project.LexiconGetExampleTranslation(translation))
        """
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        # Translation is a MultiString
        tr = ITsString(translation.Translation.get_String(WSHandle)).Text
        return tr or u""

    
    #  (Analysis WS fields)

    def LexiconGetSenseGloss(self, sense, languageTagOrHandle=None):
        """
        Returns the gloss for the sense in the Default Analysis WS or
        other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        # MultiUnicodeAccessor
        gloss = ITsString(sense.Gloss.get_String(WSHandle)).Text
        return gloss or u""

        
    def LexiconSetSenseGloss(self, sense, gloss, languageTagOrHandle=None):
        """
        Set the Default Analysis gloss for the given sense:
        
            - gloss must be unicode.
            - languageTagOrHandle specifies a different writing system.
        """

        if not self.writeEnabled: raise FP_ReadOnlyError

        if not sense: raise FP_NullParameterError()
        
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        # MultiUnicodeAccessor
        # set_String handles building a tss for us.
        sense.Gloss.set_String(WSHandle, gloss)
        return
    
    
    def LexiconGetSenseDefinition(self, sense, languageTagOrHandle=None):
        """
        Returns the definition for the sense in the Default Analysis WS or
        other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        # Definition is a MultiString
        defn = ITsString(sense.Definition.get_String(WSHandle)).Text
        return defn or u""

    #  (Non-string types)
    
    
    def LexiconGetSensePOS(self, sense):
        """
        Returns the part of speech abbreviation for the sense.
        """
        if sense.MorphoSyntaxAnalysisRA != None:
            return sense.MorphoSyntaxAnalysisRA.InterlinearAbbr
        else:
            return ""

            
    def LexiconGetSenseSemanticDomains(self, sense):
        """
        Returns a list of Semantic Domain objects belonging to the sense.
        ToString() and Hvo are available.
        """

        ## SemanticDomainsRC::
        ##      Count
        ##      Add(Hvo)
        ##      Contains(Hvo)
        ##      Remove(Hvo)
        ##      RemoveAll()
        
        return list(sense.SemanticDomainsRC)

        
    def LexiconEntryAnalysesCount(self, entry):
        # This is replicated from LexEntry.EntryAnalysesCount (v8.0.10)
        # JohnT: You could call it by reflection (it's actually a public
        # method which any instance of ILexEntry will implement; 
        # but it's not part of the interface ILexEntry, and you can't 
        # cast to LexEntry outside the LCM assembly because LexEntry 
        # is internal).
        # Assuming you have a reference to PalasoUIWindowsForms and are 
        # using ReflectionHelper, you should be able to get it with
        # (int)ReflectionHelper.GetProperty(someILexEntry, "EntryAnalysesCount").
        """
        Returns a count of the occurences of the entry in the text corpus.

        NOTE: As of Fieldworks 8.0.10 this calculation can be slightly off
        (the same analysis in the same text segment is only counted once),
        but is the same as reported in Fieldworks in the Number of Analyses
        column. See LT-13997.
        """
        count = 0
        forms = list()
        if entry.LexemeFormOA:
            forms.append(entry.LexemeFormOA)
        for mfo in entry.AlternateFormsOS:
            forms.append(mfo)
        for mfo in forms:
            for cmo in mfo.ReferringObjects:
                if self.project.ClassIsOrInheritsFrom(cmo.ClassID,
                                                 WfiMorphBundleTags.kClassId):
                    c = IWfiAnalysis(cmo.Owner).OccurrencesInTexts.Count
                    #report.Info(u"   %s = %i" % (ITsString(IWfiAnalysis(cmo.Owner).ChooserNameTS).Text, c))
                    count += c
        return count

    # --- Lexicon: field functions ---

    def GetCustomFieldValue(self, senseOrEntryOrHvo, fieldID):
        """
        Returns the field value for String, MultiString and Integer fields.
        Returns None for other field types.
        """

        if not senseOrEntryOrHvo: raise FP_NullParameterError()
        if not fieldID: raise FP_NullParameterError()

        try:
            hvo = senseOrEntryOrHvo.Hvo
        except AttributeError:
            hvo = senseOrEntryOrHvo
            
        # Adapted from XDumper.cs::GetCustomFieldValue
        mdc = self.project.MetaDataCacheAccessor
        cellarPropertyType = mdc.GetFieldType(fieldID)

        if cellarPropertyType in FLExLCM.CellarStringTypes:
            return ITsString(self.project.DomainDataByFlid.\
                             get_StringProp(hvo, fieldID))
        elif cellarPropertyType in FLExLCM.CellarUnicodeTypes:
            mua = self.project.DomainDataByFlid.get_MultiStringProp(hvo, fieldID)
            return ITsString(mua.BestAnalysisVernacularAlternative)

        elif cellarPropertyType == CellarPropertyType.Integer:
            return self.project.DomainDataByFlid.get_IntProp(hvo, fieldID)
            
        return None

        
    def LexiconFieldIsStringType(self, fieldID):
        """
        Returns True if the given field is a string type suitable for use
        with LexiconAddTagToField(), otherwise returns False.
        """
        if not fieldID: raise FP_NullParameterError()
        
        mdc = self.project.MetaDataCacheAccessor
        cellarPropertyType = mdc.GetFieldType(fieldID)
        return cellarPropertyType in FLExLCM.CellarStringTypes

        
    def LexiconGetFieldText(self, senseOrEntryOrHvo, fieldID):
        """
        Return the text value for the given entry/sense and field ID.
        Provided for use with custom fields.
        """
        if not senseOrEntryOrHvo: raise FP_NullParameterError()
        if not fieldID: raise FP_NullParameterError()

        value = self.GetCustomFieldValue(senseOrEntryOrHvo, fieldID)

        if value and value.Text != u"***":
            return value.Text
        else:
            return u""
        
        
    def LexiconSetFieldText(self, senseOrEntryOrHvo, fieldID, text, languageTagOrHandle=None):
        """
        Set the text value for the given entry/sense and field ID.

        NOTE: writes the string in one writing system only (defaults
        to the default analysis WS.)
        Provided for use with custom fields.
        """

        if not self.writeEnabled: raise FP_ReadOnlyError()

        if not senseOrEntryOrHvo: raise FP_NullParameterError()
        if not fieldID: raise FP_NullParameterError()
        
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)

        try:
            hvo = senseOrEntryOrHvo.Hvo
        except AttributeError:
            hvo = senseOrEntryOrHvo

        mdc = self.project.MetaDataCacheAccessor
        if mdc.GetFieldType(fieldID) != CellarPropertyType.String:
            raise FP_ParameterError("LexiconSetFieldText: field is not String type")

        tss = TsStringUtils.MakeString(text, WSHandle)

        try:
            self.project.DomainDataByFlid.SetString(hvo, fieldID, tss)
        except LcmInvalidFieldException as msg:
            # This exception indicates that the project is not in write mode
            raise FP_ReadOnlyError()


    def LexiconSetFieldInteger(self, senseOrEntryOrHvo, fieldID, integer):
        """
        Set the integer value for the given entry/sense and field ID.
        Provided for use with custom fields.
        """

        if not self.writeEnabled: raise FP_ReadOnlyError()

        if not senseOrEntryOrHvo: raise FP_NullParameterError()
        if not fieldID: raise FP_NullParameterError()
        
        try:
            hvo = senseOrEntryOrHvo.Hvo
        except AttributeError:
            hvo = senseOrEntryOrHvo

        mdc = self.project.MetaDataCacheAccessor
        if mdc.GetFieldType(fieldID) != CellarPropertyType.Integer:
            raise FP_ParameterError("LexiconSetFieldInteger: field is not Integer type")

        if self.project.DomainDataByFlid.get_IntProp(hvo, fieldID) != integer:
            try:
                self.project.DomainDataByFlid.SetInt(hvo, fieldID, integer)
            except LcmInvalidFieldException as msg:
                # This exception indicates that the project is not in write mode
                raise FP_ReadOnlyError()


    def LexiconAddTagToField(self, senseOrEntryOrHvo, fieldID, tag):
        """
        Appends the tag string to the end of the given field in the
        sense or entry inserting a semicolon between tags.
        If the tag is already in the field then it isn't added.
        """

        s = self.LexiconGetFieldText(senseOrEntryOrHvo, fieldID)
                
        if s:
            if tag in s: return
            newText = "; ".join((s, tag))
        else:
            newText = tag

        self.LexiconSetFieldText(senseOrEntryOrHvo,
                                 fieldID,
                                 newText)

        return
    

    # --- Lexicon: Custom fields ---
    
    def __GetCustomFieldsOfType(self, classID):
        """
        Generator for finding all the custom fields at Sense or Entry level.
        Returns tuples of (flid, label)
        """

        # The MetaDataCache defines the project structure: we can
        # find the custom fields in here.
        mdc = self.project.MetaDataCacheAccessor
        for flid in mdc.GetFields(classID, False, -1):
            if self.project.GetIsCustomField(flid):
                yield ((flid, mdc.GetFieldLabel(flid)))

    def __FindCustomField(self, classID, fieldName):
        for flid, name in self.__GetCustomFieldsOfType(classID):
            if name == fieldName:
                return flid
        return None

    def LexiconGetEntryCustomFields(self):
        """
        Returns a list of the custom fields defined at Entry level.
        Each item in the list is a tuple of (flid, label)
        """
        return list(self.__GetCustomFieldsOfType(LexEntryTags.kClassId))

    def LexiconGetSenseCustomFields(self):
        """
        Returns a list of the custom fields defined at Sense level.
        Each item in the list is a tuple of (flid, label)
        """
        return list(self.__GetCustomFieldsOfType(LexSenseTags.kClassId))

    def LexiconGetEntryCustomFieldNamed(self, fieldName):
        """
        Return the entry-level field ID given its name.

        NOTE: fieldName is case-sensitive.
        """
        return self.__FindCustomField(LexEntryTags.kClassId, fieldName)

    def LexiconGetSenseCustomFieldNamed(self, fieldName):
        """
        Return the sense-level field ID given its name.

        NOTE: fieldName is case-sensitive.
        """
        return self.__FindCustomField(LexSenseTags.kClassId, fieldName)

        
    # --- Reversal Indices ---

    def ReversalIndex(self, languageTag):
        """
        Returns the ReversalIndex that matches the given languageTag string
        (eg 'en'). Returns None if there is no reversal index for
        that writing system.
        """
        languageTag = self.__NormaliseLangTag(languageTag)
        
        for ri in self.lexDB.ReversalIndexesOC:
            #print ri.WritingSystem
            if self.__NormaliseLangTag(ri.WritingSystem) == languageTag:
                return ri

        return None

    def ReversalEntries(self, languageTag):
        """
        Returns an iterator for the reversal entries for the given language
        tag (eg 'en'). Returns None if there is no reversal index for
        that writing system.
        """
        ri = self.ReversalIndex(languageTag)
        if ri:
            return iter(ri.EntriesOC)
        else:
            return None

    def ReversalGetForm(self, entry, languageTagOrHandle=None):
        """
        Returns the citation form for the reversal entry in the Default
        Vernacular WS or other WS as specified by languageTagOrHandle.
        """
        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        form = ITsString(entry.ReversalForm.get_String(WSHandle)).Text
        return form or u""

    def ReversalSetForm(self, entry, form, languageTagOrHandle=None):
        """
        Set the Default Analysis reversal form for the given reversal entry:
        
            - form must be unicode.
            - languageTagOrHandle can be used to specify a different writing system.
        """

        if not self.writeEnabled: raise FP_ReadOnlyError
        
        if not entry: raise FP_NullParameterError()

        WSHandle = self.__WSHandleAnalysis(languageTagOrHandle)
        
        # ReversalForm is a MultiUnicodeAccessor
        # set_String handles building a tss for us.
        entry.ReversalForm.set_String(WSHandle, form)
        return
    
    # --- Texts ---

    def TextsNumberOfTexts(self):
        return self.ObjectCountFor(ITextRepository)
        
    def TextsGetAll(self, supplyName=True, supplyText=True):
        """
        A Generator that returns tuples of (Name, Text) where:
        
            - Name is the best vernacular or analysis name.
            - Text is a string with newlines separating paragraphs.
            
        Passing supplyName/Text=False returns only the texts or names.
        """
        
        if not supplyText:
            for t in self.ObjectsIn(ITextRepository):
                yield ITsString(t.Name.BestVernacularAnalysisAlternative).Text
        else:
            for t in self.ObjectsIn(ITextRepository):
                content = []
                if t.ContentsOA:
                    for p in t.ContentsOA.ParagraphsOS:
                        if ITsString(p.Contents).Text:
                            content.append(ITsString(p.Contents).Text)
                
                if supplyName:
                    name = ITsString(t.Name.BestVernacularAnalysisAlternative).Text
                    yield name, u"\n".join(content)        
                else:                
                    yield u"\n".join(content)        

