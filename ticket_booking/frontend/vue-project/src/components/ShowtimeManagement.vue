<template>
    <div class="showtime-management">
      <h2>Showtime Management</h2>
  
      <!-- Form to add/edit showtime -->
      <form @submit.prevent="submitShowtime">
        <div class="form-group">
          <label for="movie">Movie:</label>
          <select v-model="selectedMovie" required>
            <option v-for="movie in movies" :key="movie.id" :value="movie.id">{{ movie.title }}</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="theatre">Theatre:</label>
          <select v-model="selectedTheatre" required>
            <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.id">{{ theatre.name }}</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="date">Date:</label>
          <input v-model="date" type="date" required>
        </div>
  
        <div class="form-group">
          <label for="time">Time:</label>
          <input v-model="time" type="time" required>
        </div>
  
        <div class="form-group">
          <label for="seats">Available Seats:</label>
          <input v-model.number="availableSeats" type="number" min="1" required>
        </div>
  
        <button type="submit">Add Showtime</button>
      </form>
  
      <!-- Showtime list -->
      <div class="showtime-list">
        <h3>Showtimes:</h3>
        <ul>
          <li v-for="showtime in showtimes" :key="showtime.id">
            {{ showtime.movieTitle }} at {{ showtime.theatreName }} - {{ showtime.date }} {{ showtime.time }} (Seats: {{ showtime.availableSeats }})
            <button @click="editShowtime(showtime)">Edit</button>
            <button @click="deleteShowtime(showtime.id)">Delete</button>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedMovie: '', // Holds the selected movie ID
        selectedTheatre: '', // Holds the selected theatre ID
        date: '', // Holds the selected date
        time: '', // Holds the selected time
        availableSeats: '', // Holds the number of available seats
        movies: [ // Array of movies (You can fetch this data from an API or Vuex store)
          { id: 1, title: 'Movie 1' },
          { id: 2, title: 'Movie 2' },
          // Add more movies here
        ],
        theatres: [ // Array of theatres (You can fetch this data from an API or Vuex store)
          { id: 1, name: 'Theatre 1' },
          { id: 2, name: 'Theatre 2' },
          // Add more theatres here
        ],
        showtimes: [] // Array to store the list of showtimes
      };
    },
    methods: {
      submitShowtime() {
        // Handle the form submission to add a new showtime
        const newShowtime = {
          id: Math.random().toString(36).substr(2, 9), // Generate a random ID (you can use a better ID generator)
          movieId: this.selectedMovie,
          movieTitle: this.movies.find(movie => movie.id === this.selectedMovie).title,
          theatreId: this.selectedTheatre,
          theatreName: this.theatres.find(theatre => theatre.id === this.selectedTheatre).name,
          date: this.date,
          time: this.time,
          availableSeats: this.availableSeats
        };
        this.showtimes.push(newShowtime);
  
        // Reset form fields
        this.selectedMovie = '';
        this.selectedTheatre = '';
        this.date = '';
        this.time = '';
        this.availableSeats = '';
      },
      editShowtime(showtime) {
        // Handle the edit functionality for a showtime
        // You can open a dialog or navigate to another page for editing
        // For simplicity, we're not implementing the edit functionality here.
      },
      deleteShowtime(showtimeId) {
        // Handle the delete functionality for a showtime
        this.showtimes = this.showtimes.filter(showtime => showtime.id !== showtimeId);
      }
    }
  };
  </script>
  
  <style>
  .showtime-management {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
  }
  
  .form-group select,
  .form-group input[type="date"],
  .form-group input[type="time"],
  .form-group input[type="number"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group button[type="submit"] {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .showtime-list {
    margin-top: 20px;
  }
  
  .showtime-list h3 {
    margin-bottom: 10px;
  }
  
  .showtime-list ul {
    list-style: none;
    padding: 0;
  }
  
  .showtime-list li {
    margin-bottom: 10px;
  }
  
  .showtime-list li button {
    background-color: #dc3545;
    color: #fff;
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .showtime-list li button.edit-button {
    background-color: #ffc107;
    margin-right: 5px;
  }
  </style>
  