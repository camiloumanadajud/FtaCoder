import os
from termcolor import colored
import xml.etree.ElementTree as ET
import re
import csv


class CodeFta():

  def __init__(self, Fta):
    self.Fta = Fta
    self.FtaPath = 'Source/FtaCoder/MappingTreaties/xml/' + Fta + '.xml'

class CodeFta(CodeFta):
  def WriteHtml(self, Topic, OutputFolder):
    self.Topic = Topic
    self.OutputFolder = OutputFolder
    print(os.getcwd())
    if not os.path.exists(self.OutputFolder):
      os.makedirs(self.OutputFolder)
    self.HtmlPath = self.OutputFolder + self.Topic + self.Fta + '.html'
    self.HtmlFile= open(OutputFolder + self.Topic + self.Fta + '.html',"w")
    print('Html file written in ' + self.HtmlPath)

class CodeFta(CodeFta):
  def WriteHtmlAllFtas(self, Topic, OutputFolder):
    self.Topic = Topic
    self.OutputFolder = OutputFolder
    self.HtmlPath = self.OutputFolder + self.Topic + '.html'
    self.HtmlFile= open(self.OutputFolder + self.Topic + '.html',"a+")
    print('Html file written in ' + self.HtmlPath)

class CodeFta(CodeFta):
  def GetFtaStructure(self):
    # Get xml tree:
    Tree = ET.parse(self.FtaPath)
    Doc = Tree.getroot()

    # Get basic Fta's information:
    self.Name = (Doc.find("meta/name")).text
    self.HtmlFile.write('<h1><center> Analysis of the ' + self.Name + ' agreement for the topic ' + self.Topic + '</center></h1>')
    self.DateSigned = (Doc.find("meta/date_signed")).text
    self.DateIntoForce = (Doc.find("meta/date_into_force")).text
    self.DateInactive = (Doc.find("meta/date_inactive")).text
    self.Status = (Doc.find("meta/status")).text

    #Initialize dummies
    self.DisputeSettlement = 1

    # Get participant countries:
    try:
      Countries = Doc.findall('meta/parties/partyisocode')
      self.CountriesList = []
      for Country in Countries:
        self.CountriesList.append(Country.text)
    except:
      print('No parties currently involved in the agreement')
    try:
      Countries = Doc.findall('meta/parties_original/partyisocode')
      self.CountriesList = []
      for Country in Countries:
        self.CountriesList.append(Country.text)
      print(colored('Signatory countries: ', 'green'))
      print(self.CountriesList)
    except:
      print('Warning: did not find signatory countries')
    
    # Get all chapters:
    self.Chapters = Doc.findall('body/')
    if self.Chapters != []:
      print(colored('Chapter titles collected','green'))
    else:
      print('The agreement is not organized in chapters')

class CodeFta(CodeFta):

  def SearchTopicChapters(self,WordsToSearch):
    self.WordsToSearch = WordsToSearch
    self.TopicDummy = []
    self.TopicChapter = []
    ChapterTitleContainingTopic = []
    Ocurrence = []
    for Chapter in self.Chapters:
      ChapterTitle = Chapter.get('name')
      for Word in self.WordsToSearch:
        try:
          Ocurrence = [m.start() for m in re.finditer('(?:^|\W)' + Word + '(?:$|\W)', ChapterTitle, re.IGNORECASE)]
        except:
          print('Chapter has no title')
        if Ocurrence != []:
          print(colored('Topic found in chapter entitled:', 'green'))
          print(Chapter.get('name'))
          self.HtmlFile.write('<h3>Topic found in chapter entitled:</h3>')
          self.HtmlFile.write('<p>'+Chapter.get('name')+'</p>')
          self.TopicDummy = 1
          ChapterTitleContainingTopic = Chapter.get('name')
          self.TopicChapter = Chapter

    # Add dummy for topic:
    if self.TopicDummy == []:
      self.TopicDummy = 0
      print('Topic Dummy = ' + str(self.TopicDummy))

class CodeFta(CodeFta):

  def DisputeArticlesInTopicChapter(self, Type):
    ChapterToBeSearched = []
    self.ArticlesWithDistputeSettlement = []
    if Type == 'TopicTreatedByWholeChapter':
      try:
        ChapterToBeSearched = self.TopicChapter
      except:
        pass
    if Type == 'TopicTreatedBySingleArticle':
      try:
        ChapterToBeSearched = self.ChapterContainingRelevantArticle
      except:
        pass
    if ChapterToBeSearched != []:
      ListOfArticles = []
      self.ArticlesWithDistputeSettlement = []
      for Chapter in self.Chapters:
        if ChapterToBeSearched == Chapter:
          ListOfArticles = Chapter.findall('article')

          for Article in ListOfArticles:
            ArticleText = Article.text
            Ocurrence = [m.start() for m in re.finditer('Disput[a-zA-Z]*', ArticleText, re.IGNORECASE)]
            if Ocurrence == []:
              Ocurrence = [m.start() for m in re.finditer('controversi[a-zA-Z]*', ArticleText, re.IGNORECASE)]
            if Ocurrence != []:
              self.ArticlesWithDistputeSettlement.append(ArticleText)

class CodeFta(CodeFta):

  def SearchTopicArticles(self):

    # Get all the articles of FTA
    ChapterArticles = []
    Ocurrence = []
    if self.TopicChapter == []:
      print(self.TopicChapter)
      if self.Chapters != []:
        for Chapter in self.Chapters:
          ChapterArticles = Chapter.findall('article')
          for Article in ChapterArticles:
            for Word in self.WordsToSearch:
              try:
                Title = Article.get('name')
                Ocurrence = [m.start() for m in re.finditer('(?:^|\W)' + Word + '(?:$|\W)', Title, re.IGNORECASE)]
                if Ocurrence != []:
                  print(colored('Topic found in article entitled:', 'green'))
                  print(Title)
                  self.HtmlFile.write('<h3>Topic found in article entitled:</h3>')
                  self.HtmlFile.write('<p>'+Title+'</p>')
                  self.TopicDummy = 1
                  print(colored('This article belongs to chapter entitled:', 'green'))
                  self.HtmlFile.write('<p>This article belongs to chapter entitled:</p>')
                  self.ChapterContainingRelevantArticle = Chapter
                  print(Chapter.get('name'))
                  self.HtmlFile.write('<p>'+Chapter.get('name')+'</p>')
              except:
                pass

class CodeFta(CodeFta):

  def CleanSentences(self):
    # Tokenize articles referring to disputes:
    if self.ArticlesWithDistputeSettlement != []:
      from nltk.tokenize import sent_tokenize
      Sentences = []
      for i in self.ArticlesWithDistputeSettlement:
        Sentence = sent_tokenize(i)
        if Sentence != []:
          Sentences = Sentences + Sentence

    # Remove some line breaks and characters (\n and \t):
      StrippedSentences = []
      for sentence in Sentences:
          a = re.sub('[\n+|\t]', ' ', sentence)
          StrippedSentences.append(a)
      Sentences = StrippedSentences

    # Keep only senteces where "dispute" is mentionned:
      self.DisputeSentences = []
      for sentence in Sentences:
        Ocurrence = [m.start() for m in re.finditer('Disput[a-zA-Z]*', sentence, re.IGNORECASE)]
        if Ocurrence == []:
          Ocurrence = [m.start() for m in re.finditer('controversi[a-zA-Z]*', sentence, re.IGNORECASE)]
        if Ocurrence != []:
          self.DisputeSentences.append(sentence)
      if Ocurrence == []:
        self.DisputeSentences.append('_')
      print(colored('Sentences referring to disputes:', 'green'))
      self.HtmlFile.write('<h4>Sentences referring to disputes:</h4>')
      print(self.DisputeSentences)
      self.HtmlFile.write('<p>'+' '.join(self.DisputeSentences)+'</p>')

    if self.ArticlesWithDistputeSettlement == []:
      print(colored('Sentences referring to disputes:', 'green'))
      self.HtmlFile.write('<h4>Sentences referring to disputes:</h4>')
      print('No sentences that mention disputes found in chapter.')
      self.HtmlFile.write('<p>No sentences that mention disputes found in chapter.</p>')

class CodeFta(CodeFta):

  def ImportClassifier(self, Vectorizer, Classifier):
    import pickle
    self.Vectorizer = pickle.load(open('Source/Classifiers/' + Vectorizer + '.pkl','rb'))
    self.Classifier = pickle.load(open('Source/Classifiers/' + Classifier + '.pkl','rb'))

class CodeFta(CodeFta):

  def ClassifySentences(self):
    #Vectorize the sentences to classify:
    if self.ArticlesWithDistputeSettlement != []:
      CountTest = self.Vectorizer.transform(self.DisputeSentences)

    #Classify the sentence:
      self.Predict = self.Classifier.predict(CountTest)
      print(colored('Classifications:', 'green'))
      self.HtmlFile.write('<h4>Classification of sentences referring to disputes:</h4>')
      print(self.Predict)
      self.HtmlFile.write('<p>'+', '.join(self.Predict)+'</p>')

class CodeFta(CodeFta):

  def DisputeSettlementDummy(self):
    if self.ArticlesWithDistputeSettlement != []:
      if any(i == 'Excludes' for i in self.Predict):
        self.DisputeSettlement = 0
      #for i in range(len(self.Predict)):
        #if self.Predict[i] == 'Includes':
          #self.DisputeSettlement = 1
      print(colored('Dispute Settlement Dummy set to:', 'green'))
      self.HtmlFile.write('<h4>Dispute Settlement Dummy set to:</h4>')
      print(self.DisputeSettlement)
      self.HtmlFile.write('<p>'+str(self.DisputeSettlement)+'</p>')
    if self.TopicDummy == 0:
      print(self.TopicDummy)
      self.DisputeSettlement = 0
      self.HtmlFile.write('<p>'+str(self.DisputeSettlement)+'</p>')


class CodeFta(CodeFta):

  def TopicArticlesInDsChapter(self):
    #Search for the dispute settlement chapter from the chapters list:
    Ocurrence = []
    DisputeSettlementChapter = []
    for Chapter in self.Chapters:
      try:
        ChapterTitle = Chapter.get('name')
        Ocurrence = [m.start() for m in re.finditer('Disput[a-zA-Z]*', ChapterTitle, re.IGNORECASE)]
        if Ocurrence == []:
          Ocurrence = [m.start() for m in re.finditer('controversi[a-zA-Z]*', ChapterTitle, re.IGNORECASE)]
      except:
        pass
      if Ocurrence != []:
        DisputeSettlementChapter.append(Chapter)
        print(colored('Dispute settlement chapter found in chapter entitled:', 'green'))
        self.HtmlFile.write('<h3>Dispute settlement chapter found in chapter entitled:</h3>')
        print(Chapter.get('name'))
        self.HtmlFile.write('<p>'+Chapter.get('name')+'</p>')
    if DisputeSettlementChapter == []:
      print(colored('Dispute settlement chapter found in chapter entitled:', 'green'))
      print('Dispute Settlement chapter not found.')
      self.HtmlFile.write('<h3>No Dispute settlement chapter</h3>')


    #Find all articles reffering to the relevant topinc in th DS chapter and extract their text:
    ListOfArticles = []
    self.ArticlesWithDistputeSettlement = []
    for Chapter in DisputeSettlementChapter:
      ListOfArticles = []
      ListOfArticles = Chapter.findall('article')

      for Article in ListOfArticles:
        ArticleText = Article.text
        for Word in self.WordsToSearch:
          Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
          if Ocurrence != []:
            self.ArticlesWithDistputeSettlement.append(ArticleText)
      #print(self.ArticlesWithDistputeSettlement)

class CodeFta(CodeFta):
  def SearchForTopicInCooperationChapter(self, KeywordsCooperationChapter):
    #Search for the cooperation chapter from the chapters list:
    Ocurrence = []
    CooperationChapter = []
    self.KeywordsCooperationChapter = KeywordsCooperationChapter
    for Chapter in self.Chapters:
      try:
        ChapterTitle = Chapter.get('name')
        Ocurrence = [m.start() for m in re.finditer('Co.*?pera.*?', ChapterTitle, re.IGNORECASE)]
        #if Ocurrence == []:
        #  Ocurrence = [m.start() for m in re.finditer('controversi[a-zA-Z]*', ChapterTitle, re.IGNORECASE)]
      except:
        pass
      if Ocurrence != []:
        CooperationChapter.append(Chapter)
        print(colored('Cooperation chapter found in chapter entitled:', 'green'))
        self.HtmlFile.write('<h3>Cooperation chapter found in chapter entitled:</h3>')
        print(Chapter.get('name'))
        self.HtmlFile.write('<p>'+Chapter.get('name')+'</p>')
    if CooperationChapter == []:
      print(colored('Cooperation chapter found in chapter entitled:', 'green'))
      print('Cooperation chapter not found.')


    #Find all articles reffering to the relevant topinc in th DS chapter and extract their text:
    ListOfArticles = []
    self.CooperationArticlesWithTopic = []
    for Chapter in CooperationChapter:
      ListOfArticles = []
      ListOfArticles = Chapter.findall('article')

      for Article in ListOfArticles:
        ArticleText = Article.text
        if self.KeywordsCooperationChapter == None:
          for Word in self.WordsToSearch:
            Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
            if Ocurrence != []:
              self.CooperationArticlesWithTopic.append(ArticleText)
              print(colored('Topic found in Cooperation chapter','green'))
              self.HtmlFile.write('<h3>Topic found in Cooperation chapter</h3>')
              print(ArticleText)
              self.HtmlFile.write('<p>'+ArticleText+'</p>')
              self.TopicDummy = 1
        else:
          for Word in self.KeywordsCooperationChapter:
            Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
            if Ocurrence != []:
              self.CooperationArticlesWithTopic.append(ArticleText)
              print(colored('Topic found in Cooperation chapter','green'))
              self.HtmlFile.write('<h3>Topic found in Cooperation chapter</h3>')
              print(ArticleText)
              self.HtmlFile.write('<p>'+ArticleText+'</p>')
              self.TopicDummy = 1

class CodeFta(CodeFta):

  def SearchForTopicInCooperationArticles(self):

    # Get all the cooperation articles of FTA
    ChapterArticles = []
    Ocurrence = []
    self.CooperationArticles = []
    if self.Chapters != []:
        for Chapter in self.Chapters:
          ChapterArticles = Chapter.findall('article')
          for Article in ChapterArticles:
            try:
              Title = Article.get('name')
              Ocurrence = [m.start() for m in re.finditer('(?:^|\W)' + 'Co.*?pera.*?' + '(?:$|\W)', Title, re.IGNORECASE)]
              if Ocurrence != []:
                print(colored('Cooperation article found in article entitled:', 'green'))
                #self.HtmlFile.write('<p>Cooperation article found in article entitled:</p>')
                print(Title)
                #self.HtmlFile.write('<p>'+Title+'</p>')
                self.CooperationArticles.append(Article)
            except:
              pass

    #Look for the topic in cooperation articles
    for Article in self.CooperationArticles:
      ArticleText = Article.text
      if self.KeywordsCooperationChapter == None:
        for Word in self.WordsToSearch:
          Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
          if Ocurrence != []:
            print(colored('Topic found in cooperation article','green'))
            self.HtmlFile.write('<h3>Topic found in cooperation article:</h3>')
            print(ArticleText)
            self.HtmlFile.write('<p>'+ArticleText+'</p>')
            self.TopicDummy = 1
      else:
        for Word in self.KeywordsCooperationChapter:
          Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
          if Ocurrence != []:
            print(colored('Topic found in cooperation article','green'))
            self.HtmlFile.write('<h3>Topic found in cooperation article:</h3>')
            print(ArticleText)
            self.HtmlFile.write('<p>'+ArticleText+'</p>')
            self.TopicDummy = 1

class CodeFta(CodeFta):

  def SearchForTopicInGeneralProvisions(self):
    #Search for General Provisions chapter
    Ocurrence = []
    GeneralProvisionsChapter = []
    for Chapter in self.Chapters:
      try:
        ChapterTitle = Chapter.get('name')
        Ocurrence = [m.start() for m in re.finditer('Gener.*? pr.*?', ChapterTitle, re.IGNORECASE)]
        if Ocurrence == []:
          Ocurrence = [m.start() for m in re.finditer('prea.*?', ChapterTitle, re.IGNORECASE)]
      except:
        pass
      if Ocurrence != []:
        GeneralProvisionsChapter.append(Chapter)
        print(colored('General provisions chapter found in chapter entitled:', 'green'))
        #self.HtmlFile.write('<p>General provisions chapter found in chapter entitled:</p>')
        print(Chapter.get('name'))
        #self.HtmlFile.write('<p>'+Chapter.get('name')+'</p>')
    if GeneralProvisionsChapter == []:
      print(colored('General Provisions chapter found in chapter entitled:', 'green'))
      print('General Provisions chapter not found.')


    #Find all articles reffering to the relevant topinc in th DS chapter and extract their text:
    ListOfArticles = []
    self.GeneralProvisionsArticlesWithTopic = []
    for Chapter in GeneralProvisionsChapter:
      ListOfArticles = []
      ListOfArticles = Chapter.findall('article')

      for Article in ListOfArticles:
        ArticleText = Article.text
        for Word in self.WordsToSearch:
          Ocurrence = [m.start() for m in re.finditer(Word, ArticleText, re.IGNORECASE)]
          if Ocurrence != []:
            self.GeneralProvisionsArticlesWithTopic.append(ArticleText)
            print(colored('Topic found in General Provisions chapter:','green'))
            self.HtmlFile.write('<h3>Topic found in General Provisions chapter:</h3>')
            print(ArticleText)
            self.HtmlFile.write('<p>'+ArticleText+'</p>')
            self.TopicDummy = 1


class CodeFta(CodeFta):

  def WriteToCsv(self):
    print(colored("FTA'summary:", 'green'))
    self.HtmlFile.write("<h2>FTA'summary:</h2>")
    print('Name , Date Signed, Date Into Force, Date Inactive, Topic Dummy, Dispute Settlement Dummy, Countries codes')
    #self.HtmlFile.write('<p>Name , Date Signed, Date Into Force, Date Inactive, Topic Dummy, Dispute Settlement Dummy, Countries codes</p>')
    print([self.Name] + [self.DateSigned] + [self.DateIntoForce] + [self.DateInactive] + [self.TopicDummy] + [self.DisputeSettlement] + self.CountriesList)
    #self.HtmlFile.write('<p>'+str(self.Name) + str(self.DateSigned) + str(self.DateIntoForce) + str(self.DateInactive) + str(self.TopicDummy) + str(self.DisputeSettlement) + '-'.join(self.CountriesList)+'</p>')
    self.HtmlFile.write('<p>Name: '+str(self.Name)+'</p>')
    self.HtmlFile.write('<p>Signed: '+str(self.DateSigned)+'</p>')
    self.HtmlFile.write('<p>In force: '+str(self.DateIntoForce)+'</p>')
    self.HtmlFile.write('<p>Inactive: '+str(self.DateInactive)+'</p>')
    self.HtmlFile.write('<p>'+self.Topic+' dummy:' +str(self.TopicDummy)+'</p>')
    self.HtmlFile.write('<p>Dispute settlement dummy:' +str(self.DisputeSettlement)+'</p>')
    self.HtmlFile.write('<p>Signatories: ' +'-'.join(self.CountriesList)+'</p>')
    print(self.OutputFolder + self.Topic + self.Fta + '.csv')
    with open(self.OutputFolder + self.Topic + self.Fta + '.csv', 'w', encoding='utf-8') as csvfile:
      filewriter = csv.writer(csvfile,delimiter=';')
      #filewriter.writerow(['Name']+ ['DateSigned'] + ['DateIntoForce'] + ['DateInactive'] + ['TopicDummy'] + ['DisputeSettlement'])
      filewriter.writerow([self.Name] + [self.DateSigned] + [self.DateIntoForce] + [self.DateInactive] + [self.TopicDummy] + [self.DisputeSettlement] + [self.CountriesList])

    self.HtmlFile.close()

def AnalizeSingleFta(Topic, FtaNumber, Keywords, OutputFolder,KeywordsCooperationChapter=None):
  Fta = CodeFta('pta_' + FtaNumber)
  Fta.WriteHtml(Topic, OutputFolder)
  Fta.GetFtaStructure()
  Fta.SearchTopicChapters(Keywords)
  Fta.DisputeArticlesInTopicChapter('TopicTreatedByWholeChapter')
  Fta.CleanSentences()
  Fta.ImportClassifier('CountVectorizerNonDSChapters', 'NaiveBayesClassifierNonDSChapters')
  Fta.ClassifySentences()
  Fta.DisputeSettlementDummy()
  Fta.TopicArticlesInDsChapter()
  Fta.CleanSentences()
  Fta.ImportClassifier('CountVectorizerDSChapters', 'NaiveBayesClassifierDSChapters')
  Fta.ClassifySentences()
  Fta.DisputeSettlementDummy()
  Fta.SearchTopicArticles()
  Fta.DisputeArticlesInTopicChapter('TopicTreatedBySingleArticle')
  Fta.CleanSentences()
  Fta.ImportClassifier('CountVectorizerNonDSChapters', 'NaiveBayesClassifierNonDSChapters')
  Fta.ClassifySentences()
  Fta.DisputeSettlementDummy()
  Fta.SearchForTopicInCooperationChapter(KeywordsCooperationChapter)
  Fta.SearchForTopicInCooperationArticles()
  Fta.SearchForTopicInGeneralProvisions()
  Fta.WriteToCsv()


def AnalizeAllFtas(Topic, Keywords, OutputFolder,KeywordsCooperationChapter=None):

  print(colored('------------------------------------', 'green'))
  print(colored('Analyzing whether FTA covers ' + Topic, 'green'))
  print(colored('------------------------------------', 'green'))

  def AnalizeSingleFta(Topic, FtaNumber, Keywords, OutputFolder):
    Fta = CodeFta('pta_' + FtaNumber)
    Fta.WriteHtmlAllFtas(Topic, OutputFolder)
    Fta.GetFtaStructure()
    Fta.SearchTopicChapters(Keywords)
    Fta.DisputeArticlesInTopicChapter('TopicTreatedByWholeChapter')
    Fta.CleanSentences()
    Fta.ImportClassifier('CountVectorizerNonDSChapters', 'NaiveBayesClassifierNonDSChapters')
    Fta.ClassifySentences()
    Fta.DisputeSettlementDummy()
    Fta.TopicArticlesInDsChapter()
    Fta.CleanSentences()
    Fta.ImportClassifier('CountVectorizerDSChapters', 'NaiveBayesClassifierDSChapters')
    Fta.ClassifySentences()
    Fta.DisputeSettlementDummy()
    Fta.SearchTopicArticles()
    Fta.DisputeArticlesInTopicChapter('TopicTreatedBySingleArticle')
    Fta.CleanSentences()
    Fta.ImportClassifier('CountVectorizerNonDSChapters', 'NaiveBayesClassifierNonDSChapters')
    Fta.ClassifySentences()
    Fta.DisputeSettlementDummy()
    Fta.SearchForTopicInCooperationChapter(KeywordsCooperationChapter)
    Fta.SearchForTopicInCooperationArticles()
    Fta.SearchForTopicInGeneralProvisions()
    Fta.WriteToCsv()

  for i in range(1,450):
    print(colored('------------------------------------', 'green'))
    print(colored('Analyzing pta_' + str(i), 'green'))
    print(colored('------------------------------------', 'green'))
    try:
      AnalizeSingleFta(Topic,str(i),Keywords,OutputFolder)
    except:
      print(colored('Error with pta_' + str(i), 'red'))

  Database = open(OutputFolder + Topic + 'CodedFtasDatabase.csv','w', encoding="utf-8")
  Database.write('Name; DateSigned; DateIntoForce; DateInactive; ' + Topic + 'Coded; DisputeSettlement \n')

  for i in range(1,450):
      try:
          DataLine = open(OutputFolder + Topic + 'pta_' + str(i) + '.csv', "r", encoding="utf-8")
          Database.write(DataLine.read())
          DataLine.close()
          os.remove(OutputFolder + Topic + 'pta_' + str(i) + '.csv')
      except:
          print('pta_' + str(i) + '.csv not found in folder')
  Database.close()

