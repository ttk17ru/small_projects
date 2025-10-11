import pyautogui as pyg
import time
from alive_progress import alive_bar
import os
from sys import exit

username = os.getlogin()
desktopDir = rf"C:\Users\{username}\Desktop"
os.chdir(desktopDir)
print(f"working dir {desktopDir}!")
print(f"Make sure the program is this path -->\n{desktopDir}")

faPass = True
print("Make sure Firefox is not working!!")

def pBar(n):
	with alive_bar(n) as bar:
		for i in range(n):
			time.sleep(0.5)
			bar()

def founded(location):
	if location:
		x, y = pyg.center(location)
		pyg.moveTo(x, y)
		pyg.click()
	else:
		print("Image not found")

# pyg.click()
def main():
	pBar(10)
	searchInp = input("SEARCH: ")
	if searchInp == "ttk@ru":
		print("sorry!\nupgraded version isn't installed yet.")
		pBar(8)
		exit()
	pBar(6)
	fireImg = pyg.locateOnScreen('fire2.png', confidence=0.9)
	x, y = pyg.center(fireImg)
	pyg.moveTo(x, y)
	pyg.click()
	pBar(6)
	pyg.write('youtube.com')
	pyg.press('enter')
	pBar(10)
	searchBImg = pyg.locateOnScreen('searchB.png', confidence=0.9)
	x3, y3 = pyg.center(searchBImg)
	pyg.moveTo(x3, y3)
	pyg.click()
	pBar(2)
	pyg.write(f'{searchInp}')
	pyg.press('enter')


main()