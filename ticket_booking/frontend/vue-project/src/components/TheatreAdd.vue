<template>
    <div>
      <!-- Display a form to add/edit theatre -->
      <form @submit.prevent="saveTheatre">
        <label>Name:</label>
        <input v-model="theatre.name" required />
        <label>Location:</label>
        <input v-model="theatre.location" required />
        <label>Contact:</label>
        <input v-model="theatre.contact" required />
        <label>Facilities:</label>
        <textarea v-model="theatre.facilities" required></textarea>
        <button type="submit">{{ editMode ? "Update" : "Add" }} Theatre</button>
      </form>
  
      <!-- Display the list of theatres -->
      <div v-if="theatres.length > 0">
        <h2>Theatres List</h2>
        <ul>
          <li v-for="(theatre, index) in theatres" :key="index">
            {{ theatre.name }} - {{ theatre.location }} - {{ theatre.contact }}
            <button @click="editTheatre(index)">Edit</button>
            <button @click="deleteTheatre(index)">Delete</button>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        theatre: {
          name: "",
          location: "",
          contact: "",
          facilities: "",
        },
        theatres: [],
        editMode: false,
        editIndex: null,
      };
    },
    methods: {
      saveTheatre() {
        if (this.editMode) {
          // Update existing theatre
          this.theatres[this.editIndex] = { ...this.theatre };
        } else {
          // Add new theatre
          this.theatres.push({ ...this.theatre });
        }
        this.clearForm();
      },
      editTheatre(index) {
        this.editMode = true;
        this.editIndex = index;
        this.theatre = { ...this.theatres[index] };
      },
      deleteTheatre(index) {
        this.theatres.splice(index, 1);
        this.clearForm();
      },
      clearForm() {
        this.editMode = false;
        this.editIndex = null;
        this.theatre = {
          name: "",
          location: "",
          contact: "",
          facilities: "",
        };
      },
    },
  };
  </script>
  