<template>
    <div class="admin-dashboard">
      <div class="overview">
        <h2>Dashboard Overview</h2>
        <div class="stats">
          <div class="stat">
            <div class="stat-value">{{ ticketSales }}</div>
            <div class="stat-label">Ticket Sales</div>
          </div>
          <div class="stat">
            <div class="stat-value">{{ numBookings }}</div>
            <div class="stat-label">Number of Bookings</div>
          </div>
          <div class="stat">
            <div class="stat-value">{{ revenue }}</div>
            <div class="stat-label">Revenue</div>
          </div>
        </div>
      </div>
      <div class="quick-links">
        <h2>Quick Links</h2>
        <div class="links">
          <router-link to="/admin/theatres" class="link">
            <v-icon>theater</v-icon>
            Manage Theatres
          </router-link>
          <router-link to="/admin/movies" class="link">
            <v-icon>movie</v-icon>
            Manage Movies
          </router-link>
          <router-link to="/admin/showtimes" class="link">
            <v-icon>schedule</v-icon>
            Manage Showtimes
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        ticketSales: 1023, // Replace with actual ticket sales data
        numBookings: 567, // Replace with actual number of bookings data
        revenue: "$12560", // Replace with actual revenue data
      };
    },
  };
  </script>
  
  <style>
  /* Add styles for the admin dashboard */
  .admin-dashboard {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: 20px;
  }
  
  .overview {
    flex: 1;
    max-width: 400px;
  }
  
  .stats {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .stat {
    text-align: center;
  }
  
  .stat-value {
    font-size: 24px;
    font-weight: bold;
  }
  
  .stat-label {
    margin-top: 5px;
    color: #888;
  }
  
  .quick-links {
    flex: 1;
    max-width: 400px;
    margin-left: 40px;
  }
  
  .links {
    display: flex;
    flex-direction: column;
  }
  
  .link {
    display: flex;
    align-items: center;
    margin: 10px 0;
    color: #2196f3;
    text-decoration: none;
  }
  
  .link v-icon {
    margin-right: 5px;
  }
  </style>
  