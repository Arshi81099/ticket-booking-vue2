<template>
    <div class="edit-theatre-container">
      <h2>Edit Theatre Details</h2>
      <form @submit.prevent="saveTheatre">
        <div class="form-group">
          <label for="name">Name:</label>
          <input v-model="name" type="text" id="name" required>
        </div>
        <div class="form-group">
          <label for="location">Location:</label>
          <input v-model="location" type="text" id="location" required>
        </div>
        <div class="form-group">
          <label for="contact">Contact:</label>
          <input v-model="contact" type="text" id="contact" required>
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <input v-model="address" type="text" id="address" required>
        </div>
        <div class="form-group">
          <label for="facilities">Facilities:</label>
          <input v-model="facilities" type="text" id="facilities" required>
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      theatre: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        name: this.theatre.name,
        location: this.theatre.location,
        contact: this.theatre.contact,
        address: this.theatre.address,
        facilities: this.theatre.facilities.join(', '),
      };
    },
    methods: {
      saveTheatre() {
        // Create an object with the updated theatre details
        const updatedTheatre = {
          name: this.name,
          location: this.location,
          contact: this.contact,
          address: this.address,
          facilities: this.facilities.split(',').map((item) => item.trim()), // Convert facilities to an array
        };
  
        // Emit the updated theatre details to the parent component to handle saving
        this.$emit('update-theatre', updatedTheatre);
      },
    },
  };
  </script>
  
  <style>
  /* Custom Styles for the component */
  
  .edit-theatre-container {
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
  