*** 需要哪些資料？ ***
格局放大，將所有可能的變因納入，不要預設哪些資訊不會影響，層別後再刪除都不遲。
一開始的output資料只有輸出dut溫度和PWM，接著新加入oven temp和BIB temp和power，我的程式需進行第一次改版。

*** 簡化你的程式？ ***
寫完程式並不會花你太多時間，但如何簡化和最大化彈性，這部分要花時間去琢磨。簡單的方式有使用function包裝每個功能、使用物件、分裝不同module或package。跑圖可以使用scripts腳本來達到自動化以及簡單維護的目的。

*** 歸納出來的流程？ ***
分成存入DB前的前段處理，和存入DB後取出的後段處理。

* Pre-DB
	1. 讀入資料，txt or csv
	2. 輸入資料也有可能是一束，要批次讀入。
	3. txt需要先擷取。
	4. 轉成dataframe格式
	5. astype(...)修正資料型式。如果有時間轉換成TimeStamp
	6. 加入額外的欄位，另外輸入或從資料得到的分群，例如：power, fan_motor
	7. Trim 需要的長度，有些等待的時間可以刪除。
	8. 存入DB或是csv

* Post-DB
	0. 輸出每個test 的profile
	1. SQL 讀出符合條件的資料
	2. 規畫統計藍圖，並建立腳本(建立取出欄位並給予欄位順序)
	3. 順序為：columns[0]: hue , columns[1:]: x, columns[1:].values: y
	4. 建立給圖function
	5. savefig
	6. bonus: stats Model
