import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# os.chdir("C:\\Users\\q845332\\data")
df = pd.read_csv("BA_Traveloka.csv")

con = duckdb.connect(database=':memory:')
con.register('booking', df)

print(df.head())

query_total_sales = """
SELECT 
    "Airlines", 
    SUM("Selling price to customer") AS Total_Sales
FROM booking
GROUP BY "Airlines"
ORDER BY Total_Sales DESC;
"""

total_sales = con.execute(query_total_sales).fetchdf()
print(total_sales)


# Plot
# plt.figure(figsize=(10, 6))
# plt.bar(total_sales['Airlines'], total_sales['Total_Sales'])
# plt.xlabel('Airlines')
# plt.ylabel('Total Sales')
# plt.title('Total Sales per Airlines')
# plt.xticks(rotation=45)
# plt.show()



query_total_seats = """
SELECT 
    "Route", 
    SUM("number of seat") AS Total_Seats
FROM booking
GROUP BY "Route"
ORDER BY Total_Seats DESC;
"""
total_seats = con.execute(query_total_seats).fetchdf()

# # Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=total_seats, x='Total_Seats', y='Route', palette='magma')
# plt.title('Total Number of Seats Sold by Route')
# plt.xlabel('Total Seats')
# plt.ylabel('Route')
# plt.show()

query_avg_ticket_fare = """
SELECT 
    "Payment method", 
    ROUND(AVG("Ticket fare from airlines"), 2) AS Avg_Ticket_Fare
FROM booking
GROUP BY "Payment method"
ORDER BY Avg_Ticket_Fare DESC;
"""
avg_ticket_fare = con.execute(query_avg_ticket_fare).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=avg_ticket_fare, x='Avg_Ticket_Fare', y='Payment method', palette='coolwarm')
# plt.title('Average Ticket Fare by Payment Method')
# plt.xlabel('Average Ticket Fare')
# plt.ylabel('Payment Method')
# plt.show()

#  Booking ID,Booking Date,Departure Date,Route,Airlines,Number of seat,Ticket fair from airlines,Selling price to customer,Payment method

query_top_routes = """
SELECT "Route", COUNT(*) as NumBookings
FROM booking
GROUP BY "Route"
ORDER BY NumBookings DESC
LIMIT 5;
"""
top_routes = con.execute(query_top_routes).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=top_routes, x='NumBookings', y='Route', palette='inferno')
# plt.title('Top 5 Routes by Number of Bookings')
# plt.xlabel('Number of Bookings')
# plt.ylabel('Route')
# plt.show()


query_avg_total_fare_route = """
SELECT "Route", AVG(TotalFare) AS AvgTotalFare
FROM (
  SELECT "Route", SUM("Ticket fare from airlines") AS TotalFare
  FROM booking
  GROUP BY "Route"
) AS Subquery
GROUP BY "Route";
"""
avg_total_fare_route = con.execute(query_avg_total_fare_route).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=avg_total_fare_route, x='AvgTotalFare', y='Route', palette='cubehelix')
# plt.title('Average Total Ticket Fare for Each Route')
# plt.xlabel('Average Total Fare')
# plt.ylabel('Route')
# plt.show()


query_top_airlines = """
SELECT 
    "Airlines", 
    COUNT(*) AS NumBookings
FROM booking
GROUP BY "Airlines"
ORDER BY NumBookings DESC
LIMIT 3;
"""
top_airlines = con.execute(query_top_airlines).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=top_airlines, x='NumBookings', y='Airlines', palette='plasma')
# plt.title('Top 3 Airlines with the Most Number of Bookings')
# plt.xlabel('Number of Bookings')
# plt.ylabel('Airlines')
# plt.show()

query_total_fare_route = """
WITH RouteFares AS (
  SELECT "Route", 
  SUM("Ticket fare from airlines") AS TotalFare
  FROM booking
  GROUP BY "Route"
)
SELECT "Route", AVG(TotalFare) AS AvgTotalFare
FROM RouteFares
GROUP BY "Route";
"""
total_fare_route = con.execute(query_total_fare_route).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=total_fare_route, x='AvgTotalFare', y='Route', palette='cividis')
# plt.title('Total Ticket Fare from Airlines for Each Route')
# plt.xlabel('Average Total Fare')
# plt.ylabel('Route')
# plt.show()

query_avg_selling_price = """
SELECT 
    "Route", 
    AVG("Selling price to customer") AS AvgSellingPrice
FROM booking
WHERE "Route" IN (
  SELECT "Route"
  FROM booking
  GROUP BY "Route"
  HAVING COUNT(*) > 5
)
GROUP BY "Route";
"""
avg_selling_price = con.execute(query_avg_selling_price).fetchdf()

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=avg_selling_price, x='AvgSellingPrice', y='Route', palette='spring')
# plt.title('Average Selling Price to Customers for Each Route')
# plt.xlabel('Average Selling Price')
# plt.ylabel('Route')
# plt.show()


query_total_seats_route = """
WITH RouteSeats AS (
  SELECT 
   "Route", 
   SUM("number of seat") AS TotalSeats
  FROM booking
  GROUP BY "Route"
)
SELECT "Route", AVG(TotalSeats) AS AvgTotalSeats
FROM RouteSeats
GROUP BY "Route";
"""
total_seats_route = con.execute(query_total_seats_route).fetchdf()

print(total_seats_route)

# Plot
# plt.figure(figsize=(10, 6))
# sns.barplot(data=total_seats_route, x='AvgTotalSeats', y='Route', palette='cool')
# plt.title('Total Number of Seats for Each Route')
# plt.xlabel('Average Total Seats')
# plt.ylabel('Route')
# plt.show()


query_ranking_routes = """
SELECT 
 "Route", 
 TotalSeats,
    RANK() OVER (ORDER BY TotalSeats DESC) AS ranking
FROM (
   SELECT 
    "Route", 
    SUM("number of seat") AS TotalSeats
   FROM booking
   GROUP BY "Route"
) AS Subquery;
"""
ranking_routes = con.execute(query_ranking_routes).fetchdf()

print(ranking_routes)

# Plot
plt.figure(figsize=(10, 8))
sns.barplot(data=ranking_routes, x='TotalSeats', y='Route', palette='autumn')
plt.title('Ranking of Each Route Based on the Total Number of Seats')
plt.xlabel('Total Seats')
plt.ylabel('Route')
plt.show()