#import modules/libaries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import os
import time


#Create class Automate 
class Automate():


	#Constructor Function that defines the webbrowser and its default settings.  Self is substitute for any object created of class Automate(), think obj == self
	def __init__(self):
		#Assign options variable to add option arguments for webdriver, these are mainly to block popups and other things that will disrupt the browser.  Default settings for chromebrowser
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--ignore-ssl-errors')
		options.add_argument('--disable-extensions')
		options.add_argument('--disable-infobars')
		options.add_argument("start-maximized")
		prefs={"profile.default_content_setting_values.notifications" : 2}
		options.add_experimental_option("prefs",prefs)
		dir_path = os.path.dirname(os.path.realpath(__file__))
		chromedriver = dir_path + "/chromedriver"
		os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome(chrome_options=options, executable_path= chromedriver)
		
	#Function to Pause browser
	def timerpractice(self):
		time.sleep(10)

	def googlesignin(self):
		#This will sign into google and will then turn of flash popups and other things that will distract browser
		url = 'https://www.google.com/accounts/Login?hl=EN=http://www.google.co.jp/'  
		self.driver.get(url)
		self.driver.find_element_by_xpath("//input[@id='identifierId']").send_keys("Blainemcmahonautomatethis")
		self.driver.find_element_by_id("identifierNext").click()
		self.driver.implicitly_wait(4)
		self.driver.find_element_by_name("password").send_keys("Python99")
		time.sleep(2)
		self.driver.find_element_by_id("passwordNext").click()
		#Goes to Fusion's website and bring it to the DPN Page
		self.driver.get("https://fusiondev/fusion/core/home.exterro")
		self.driver.get("https://fusiondev/fusion/legalhold/manageLegalHold.exterro")
		#time.sleep(9)
		#test = self.driver.find_elements_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/pagination/arrow-next.gif"]')
		time.sleep(2)
		#Now browser will need to change emplyee status from drop down menu
		result_per_page = Select(self.driver.find_element_by_id("rowsDisplayed"))
		result_per_page.select_by_visible_text("250")
		time.sleep(2)

		self.driver.implicitly_wait(2)

    #Function to go change status of terminated employees 
	def gotowebsite(self,mylist={}):
		
		
		self.driver.implicitly_wait(2)

		

#-------------------------Function to go through all DPN's and select terminated employee's and deactive buttons-----------------------------------------------

		#Variable used to control index of the list 
		index = 0

		while (index <= len(mylist)):

			print(index)

			#Give browser time to load in elements 
			time.sleep(1)

			#This will bring me to the first DPN in fusion dev 
			dpn1 = self.driver.find_element_by_link_text('%s' % mylist[index]) 
			dpn1.click()


			#Will go into the manage reminders tab
			self.driver.implicitly_wait(4)
			manage_reminder = self.driver.find_element_by_id("dynamicTabs_Manage Reminders")
			manage_reminder.click()
			time.sleep(1)


			#Change resend active and escalate to deactivated
			self.driver.implicitly_wait(3)
			time.sleep(3)
			escalate_active_button = self.driver.find_element_by_class_name("tab_hd").click()
			#wait for browser to load in elements 
			self.driver.implicitly_wait(4)
			time.sleep(3)
			reactivate_button = self.driver.find_element_by_class_name("tab_hd_l")
			reactivate_button.click()
			time.sleep(8)
			self.driver.implicitly_wait(4)
			#This will change the search criteria to unemployed people
			search_custodians = self.driver.find_element_by_link_text('Search Legal Hold Custodians').click()

			#Now browser will need to change emplyee status from drop down menu
			drop_down_list = Select(self.driver.find_element_by_id("employmentStatuses"))
			drop_down_list.select_by_visible_text("terminated")


			#Click the search button to update list to terminated employees
			self.driver.find_element_by_xpath('//a[img/@src="/fusion/StaticContent/images/search/search.gif"]').click()
			self.driver.implicitly_wait(4)					
			
			#Put the driver to sleep to allow elements to be refreshed into page
			time.sleep(5)

#------------------------------------------If There is more than one custodian--------------------------------------------------------------------------
			
			#Need to check if there is multiple pages of custodians 
			arrow = self.driver.find_elements_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/pagination/arrow-next.gif"]')
			arrow_counter = 0

			#Function to handle when there is more than one page in a DPN 
			self.pagecycle(arrow,arrow_counter)
				
#---------------------------------------------Below is rest of code to finish the program-------------------------------------------------------------
			time.sleep(2)
			#Find the little x button to shrink webpage and give access to custodians to be clicked
			self.driver.find_element_by_xpath("//img[contains(@title,'Close')]").click()

			#Boolean object to check to see if there are terminated custodians or not in DPN 
			custodian_list = self.driver.find_elements_by_id("checkAllInPage")

			#This will check the custodian list to see if it is empty or not 
			if not custodian_list:
				#Iterate the custodian index
				index = index + 1
				#Go back to the DPN Page 
				self.driver.get("https://fusiondev/fusion/legalhold/manageLegalHold.exterro")
				#Continue the program 	
				continue
			
			#Else all of the terminated custodians notifications will be disabled 
			else:

				#Will select all custodains on the page 
				select_all_in_page = self.driver.find_element_by_id("checkAllInPage")
				select_all_in_page.click()

				#Apply to selected custodians 
				self.driver.find_element_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/genomeicon/apply_n.gif"]').click()

				#navigate to the next DPN on the list
				self.driver.get("https://fusiondev/fusion/legalhold/manageLegalHold.exterro")
				#index counter 
				index = index + 1 

	

	def pagecycle(self,arrow,arrow_counter):
		
		while arrow:

				time.sleep(4)

				#index variable to track amount of pages 
				arrow_counter = arrow_counter + 1


				#Find the little x button to shrink webpage and give access to custodians to be clicked
				self.driver.find_element_by_xpath("//img[contains(@title,'Close')]").click()

			
				#Will select all custodains on the page 
				select_all_in_page = self.driver.find_element_by_id("checkAllInPage")
				select_all_in_page.click()

				#Apply to selected custodians 
				self.driver.find_element_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/genomeicon/apply_n.gif"]').click()

				time.sleep(3)
				self.driver.implicitly_wait(4)
				top_page=self.driver.find_element_by_tag_name('html')
				top_page.send_keys(Keys.UP)
				time.sleep(8)
				#This will change the search criteria to unemployed people
				search_custodians = self.driver.find_element_by_link_text('Search Legal Hold Custodians').click()

				time.sleep(3)

				#Now browser will need to change emplyee status from drop down menu
				drop_down_list = Select(self.driver.find_element_by_id("employmentStatuses"))
				drop_down_list.select_by_visible_text("terminated")


				#Click the search button to update list to terminated employees
				self.driver.find_element_by_xpath('//a[img/@src="/fusion/StaticContent/images/search/search.gif"]').click()
				self.driver.implicitly_wait(4)
					
				#Put the driver to sleep to allow elements to be refreshed into page
				time.sleep(6)
				

				#for loopbreaker in range(arrow_counter):
				#	print(arrow_counter)
				end_page = self.driver.find_element_by_tag_name('html')
				end_page.send_keys(Keys.END)

				time.sleep(8)
					
				page_number = self.driver.find_element_by_xpath("""//*[@id="manageRemainderMainBodyDiv"]/table[3]/tbody/tr/td[2]/table/tbody/tr/td[3]/input""")
				time.sleep(8)
				page_number.send_keys(Keys.BACKSPACE)
				time.sleep(2)
				page_number.send_keys(arrow_counter)
				time.sleep(2)
				page_number.send_keys(Keys.RETURN)

					#self.driver.find_element_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/pagination/arrow-next.gif"]').click()

				time.sleep(5)

				arrow = self.driver.find_elements_by_xpath('//a[img/@src="/fusion/StaticContent/images/compass/pagination/arrow-next.gif"]')			

	#Function to close down browser
	def teardown(self):
		self.driver.close()


#Main Function will execute here creating object of class Automate and using the gotowebsite function
if __name__ == "__main__":
	
	List_1 =		['AS_TEST_AUG', 'AS-TEST-2','CA DPN for Pradaxa Litigation (LOM)','DE DPN for Aggrenox (Antitrust Litigation)(LOM) - 01/30/2014','DE DPN for Aggrenox (Antitrust Litigation)(LOM) - 01/31/2014','DE DPN for Aggrenox (Kremers) (LOM)','DE DPN for Canale, Lee vs. BIPI','DE DPN for Diehl vs BIPI, et al (Tradjenta) (LOM) - TEST','DE DPN for FTC / CID (Aggrenox-Mirapex) (LOM)','DE DPN for Jardiance, Synjardy, Glyxambi Litigation','DE DPN for Linagliptin (Tradjenta & Jentadueto) (LOM)',
					'DE DPN for Linagliptin Product Liability Dispute','DE DPN for Nintedanib in IPF Study 1199.187','US DPN For Nintedanib/OFEV Expanded Access Program (“EAP”)','DE DPN for Pradaxa Litigation (LOM)','DE DPN for Pradaxa Patent Litigation (LOM)','DE DPN for Project Marengo','DE DPN for Vulpis v. BIPI, et al. (Jentadueto)','Sean First DPN','TEST settings','US DPN For Nintedanib/OFEV Expanded Access Program (“EAP”)','US DPN for Pradaxa Litigation (LOM)','US DPN for Reglan/Metoclopramide v RLI & BVL -05/2/2010 Acknowledgement']

	List_2 =		['US DPN for Adalimumab Biosimilar Product DISP-000362','US DPN for Aggrenox (Antitrust Litigation)(LOM) - 01/10/2014','US DPN for Aggrenox (Kremers) (LOM)','US DPN for Amaral, Peter (Sodexo)','US DPN for Angarola, Alison v. BIPI','US DPN for Barseghian, Deric vs. BIRI & RLI, et. al. (Dexamethasone)',
					'US DPN for Bay Area Surgical Group, Inc. et al v. Aetna','US DPN for Canale, Lee vs. BIPI','US DPN for Cassady, Chris vs BI Fremont','US DPN for Chin, Wanda vs BIPI','US DPN for Christman, Richard v. BIPI','US DPN for Cravens, Cedric vs. BIPI','US DPN for Del Canto, Tiffany v. BIPI','US DPN for Devlin, Mary Ellen v. BIUSA',
					'US DPN for DOJ Investigation: Medicaid Drug Rebate Program (LOM)','US DPN for DOJ Subpoena - 501(c)(3) Organizations','US DPN for Francis, Noah vs BIPI','US DPN for Frank Cortazzo et al. vs. BIPI','US DPN for Franklin Livestock, Inc. vs BIVI (US6101-5120000000)','US DPN for Fredericks, Ronald vs. BIPI',
					'US DPN for FTC / CID (Aggrenox-Mirapex) (LOM) - 12/28/2010','US DPN for Geiger, Tyeson L. vs BIVI','US DPN for Gitschier, Tracy vs. BIPI','US DPN for Gitthens, Brian vs BI Vetmedica','US DPN for Haile, Enoch vs BIFI']


	List_3 = 	['US DPN for Heikes, Troy vs. BIVI, et al. (Rhinomune & Vetera EWT + WNV)','US DPN for Hirst, Kathleen vs BIUSA','US DPN for Janine Stalder v. Boehringer Ingelheim Vetmedica, Inc., et al (US6101-5120000000)','US DPN for Jardiance, Synjardy, Glyxambi Litigation',
					'US DPN for Jenkins, Andrea vs BIPI','US DPN for Jessie, Erica vs. BIPI','US DPN for Linagliptin (Tradjenta & Jentadueto) (LOM)','US DPN for Linagliptin Product Liability Dispute','US DPN for Loritz-Acker, Victoria v. BIPI','US DPN for May, Daniel v. BIVI',
					'US DPN for Meyers, Troy v. BIPI, et al (Mobic)','US DPN for Mirapex General Litigation/BIPI (Venable)','US DPN for Morrison, et al v. BIVI, et al','US DPN for Nardello, Jennifer vs. BIPI','US DPN for Nintedanib in IPF Study 1199.187',"US DPN for O'Connor, Katherine vs BIPI",'US DPN for OFCCP Investigation and Audits BIPI 2016','US DPN for OFCCP Investigations and Audits-BIVI','US DPN for PCV-2 Vaccines (IngelvacCircoFLEX)',
					'US DPN for Physicians Healthsource Inc vs BIPI']

	List_4 =['US DPN for Pollard, Velma - Demand Letter (50200/530102)','US DPN for Pradaxa Patent Litigation (LOM)','US DPN for Project Marengo','US DPN for Reglan/Metoclopramide v RLI & BVL - 05/19/2010','US DPN for Reglan/Metoclopramide v RLI & BVL - 05/19/2010 No Acknowledgement','US DPN for Roberts, Rita vs. BIPI-EEOC Charge','US DPN for Ronald Rampersad v. BIVI','US DPN for Schaefer v. BIVI, et al (Mycopar)','US DPN for Sherry Moon vs BIPI - Mirapex',
					'US DPN for Sorcek, Ronald v. BIPI','US DPN for Sutherland, Lindsey R. vs. BIPI','US DPN for Swain, Karlotta v. BIPI','US DPN for Swedberg, Ken v. BIPI','US DPN for The Literature Store v BI Vetmedica','US DPN for Vigeana Sanon vs. BIPI','US DPN for Wang, Elaine',
					'US DPN for Williams, Jana M. vs BIPI','US DPN For Wilson, Rhonda vs. BI Vetmedica et al','US DPN for Wise, Alice vs BIPI','US DPN for Wright, Krystee v. BIVI','US DPN for Wyszynski, Phil vs BIPI','US DPN For: Loui, Rachel vs BIPI']




	obj = Automate()
	obj.googlesignin()
	obj.gotowebsite(List_1)
	obj.gotowebsite(List_2)
	obj.gotowebsite(List_3)
	obj.gotowebsite(List_4)
