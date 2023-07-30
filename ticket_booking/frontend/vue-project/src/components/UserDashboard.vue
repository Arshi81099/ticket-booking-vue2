<template>
  <div class="dashboard-container">
    <!-- Personalized Dashboard -->
    <h2>Welcome, {{ user.name }}</h2>
    <p>Email: {{ user.email }}</p>

    <!-- Update Personal Details Form -->
    <h3>Update Personal Details</h3>
    <form @submit.prevent="updateDetails" class="update-form">
      <label for="displayName">Name:</label>
      <input type="text" v-model="name" id="name" >
      <br>
      <label for="email">Email:</label>
      <input type="email" v-model="email" id="email" >
      <br>
      <label for="password">Password:</label>
      <input type="password" v-model="password" id="password" >
      <br>
      <button type="submit">Update Details</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user : null,
      name : "",
      // email : "",
      password : "",
      n_email : ""
    };
  },
  computed: {
    updateData() {
      return {
        name: this.name,
        // n_email: this.email,
        email : sessionStorage.getItem("email"),
        password: this.password,
      };
    },
  },
  mounted() {
    this.fetchUser()
  },
  methods: {
    async fetchUser(){
      const email = sessionStorage.getItem('email') || localStorage.getItem('email');
      try {
            const data = {"email": email}
            const response = await this.$http.get('user', {params: data});
          this.user = response.data;
          console.log(this.user)
        } catch (error) {
          console.error('Error fetching theatre:', error);
        }
    },
    async updateDetails() {
      // const old_email = sessionStorage.getItem("email")
      // const formData = new FormData();
      //     formData.append('name', this.name);
      //     formData.append('n_email', this.email);
      //     formData.append('email', old_email);
      //     formData.append('password', this.password);
      const response = await this.$http.put('user', this.updateData);
              if (response.status === 201) {
  
                  window.alert("details updated successfully!")
                  this.$router.push('/userdashboard');
                  window.location.reload()
                } else if (response.status === 400) {
                      console.log(response.data)
                      const error_message = response.data.error_message;
                      // console.log(error_message)
                      window.alert(error_message)
                      // console.log(response.text)
                  }
                  else{
                    console.log(response.status, response.data.text)
                  }
    },
    changePassword() {

      const newPasswordData = {
        newPassword: this.newPassword,
      };
      this.newPassword = '';
    },
  },
};
</script>

<style>
/* Custom Styles for the component */

/* Dashboard Container */
.dashboard-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #000;
  background-color: pink;
  color: black;
  border-radius: 10px;
}

/* Update Personal Details Form */
.update-form {
  margin-top: 10px;
}

/* Form Labels */
label {
  font-weight: bold;
  margin-right: 5px;
}

/* Form Inputs */
input {
  padding: 5px;
  margin-bottom: 10px;
}

/* Form Buttons */
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
