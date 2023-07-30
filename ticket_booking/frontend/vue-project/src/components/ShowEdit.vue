<template>
    <div class="edit-show-container">
      <h2>Edit Show Details</h2>
      <form @submit.prevent="saveShow">
        <div class="form-group">
          <label for="movie">Movie:</label>
          <select v-model="selectedMovie" id="movie">
            <option v-for="movie in movies" :key="movie.id" :value="movie.id">{{ movie.title }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="theatre">Theatre:</label>
          <select v-model="selectedTheatre" id="theatre">
            <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.id">{{ theatre.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date">Date:</label>
          <input v-model="date" type="date" id="date">
        </div>
        <div class="form-group">
          <label for="time">Time:</label>
          <input v-model="time" type="time" id="time">
        </div>
        <div class="form-group">
          <label for="seats">Available Seats:</label>
          <input v-model.number="availableSeats" type="number" id="seats">
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Object,
        required: true,
      },
      movies: {
        type: Array,
        required: true,
      },
      theatres: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        selectedMovie: this.show.movieId,
        selectedTheatre: this.show.theatreId,
        date: this.show.date,
        time: this.show.time,
        availableSeats: this.show.availableSeats,
      };
    },
    methods: {
      saveShow() {
        // Create an object with the updated show details
        const updatedShow = {
          movieId: this.selectedMovie,
          theatreId: this.selectedTheatre,
          date: this.date,
          time: this.time,
          availableSeats: this.availableSeats,
        };
  
        // Emit the updated show details to the parent component to handle saving
        this.$emit('update-show', updatedShow);
      },
    },
  };
  </script>
  
  <style>
  /* Custom Styles for the component */
  
  .edit-show-container {
    margin: 20px;
    padding: 20px;
    border: 1px solid #000;
    background-color: pink;
    color: black;
    border-radius: 10px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  label {
    font-weight: bold;
    margin-right: 5px;
  }
  
  select,
  input {
    padding: 5px;
  }
  
  button {
    padding: 10px 20px;
    background-color: black;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #333;
  }
  </style>
  