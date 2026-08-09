**Q1: Find the total spending on players for each team;**
**Q1: Hər komanda üçün oyunçulara xərclənən ümumi məbləği tapın:**


```sql
SELECT Team, SUM(price_in_cr) AS 'Total Spending'
FROM IPLPlayers
GROUP BY Team
ORDER BY 'Total Spending' DESC
```

<img width="502" height="400" alt="Query Result" src="https://github.com/user-attachments/assets/f5c456ca-87f0-4782-87df-c114a1c58aed" />
