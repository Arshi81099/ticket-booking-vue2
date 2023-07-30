<template>
    <div>
      <!-- Add button to open the form/modal for adding a new theatre -->
      <button @click="showAddTheatreForm">Add Theatre</button>
  
      <!-- Table or list to display the existing theatres -->
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Contact</th>
            <th>Facilities</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(theatre, index) in theatres" :key="index">
            <td>{{ theatre.name }}</td>
            <td>{{ theatre.location }}</td>
            <td>{{ theatre.contact }}</td>
            <td>{{ theatre.facilities }}</td>
            <td>
              <button @click="editTheatre(index)">Edit</button>
              <button @click="deleteTheatre(index)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Form or modal for adding/editing theatres -->
      <div v-if="showForm">
        <form @submit.prevent="saveTheatre">
          <!-- Add input fields for theatre details: name, location, contact, facilities -->
          <input v-model="newTheatre.name" required>
          <input v-model="newTheatre.location" required>
          <input v-model="newTheatre.contact" required>
          <input v-model="newTheatre.facilities" required>
  
          <button type="submit">Save</button>
          <button @click="cancelForm">Cancel</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        theatres: [], // Array to store all theatres
        newTheatre: {
          name: '',
          location: '',
          contact: '',
          facilities: '',
        },
        showForm: false, // To control visibility of the form/modal
      };
    },
    methods: {
      showAddTheatreForm() {
        // Show the form/modal for adding a new theatre
        this.showForm = true;
        // Clear the input fields
        this.newTheatre = {
          name: '',
          location: '',
          contact: '',
          facilities: '',
        };
      },
      saveTheatre() {
        // Add or edit the theatre depending on whether an index is provided
        if (this.editIndex === null) {
          // Add new theatre
          this.theatres.push(this.newTheatre);
        } else {
          // Edit existing theatre
          this.theatres[this.editIndex] = this.newTheatre;
        }
        // Hide the form/modal after saving
        this.showForm = false;
      },
      editTheatre(index) {
        // Show the form/modal for editing a theatre
        this.showForm = true;
        this.editIndex = index;
        // Set the input fields with the current theatre details for editing
        this.newTheatre = { ...this.theatres[index] };
      },
      deleteTheatre(index) {
        // Delete a theatre from the array
        this.theatres.splice(index, 1);
      },
      cancelForm() {
        // Hide the form/modal without saving
        this.showForm = false;
      },
    },
  };
  </script>
  
  <style>
  /* Custom styles for the TheatreManagement component */
  
  /* Style the table */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  /* Style the form/modal */
  form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  input[type="text"],
  input[type="number"] {
    margin-bottom: 10px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    padding: 10px 15px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"] {
    background-color: #28a745;
  }
  
  button[type="submit"]:hover {
    background-color: #218838;
  }
  
  button[type="button"] {
    margin-right: 10px;
    background-color: #dc3545;
  }
  
  button[type="button"]:hover {
    background-color: #c82333;
  }
  </style>
  