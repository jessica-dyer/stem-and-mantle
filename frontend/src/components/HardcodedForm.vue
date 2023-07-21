<template>
    <v-form>
        <v-container class="custom-container">
      <v-row align="center">
        <v-col cols="12">
          <h1 class="form-title">ENTER CLIMB</h1>
        </v-col>
      </v-row>
        <v-text-field
          label="Gym"
          v-model="gym"
          outlined
        ></v-text-field>
  
        <v-row>
          <v-col cols="12">
            <v-date-picker
              v-model="date"
              label="Date"
              outlined
            ></v-date-picker>
          </v-col>
        </v-row>
  
        <v-autocomplete
          label="Grade given"
          v-model="givenGrade"
          :items="grades"
          outlined
        ></v-autocomplete>
  
        <v-autocomplete
          label="Grade feels like"
          v-model="gradeFeelsLike"
          :items="grades"
          outlined
        ></v-autocomplete>
  
        <v-select
          label="Style"
          v-model="selectedStyle"
          :items="['Top Rope', 'Lead']"
          outlined
        ></v-select>
  
        <v-text-field
          label="Number of takes"
          v-model="numberValue"
          type="number"
          outlined
        ></v-text-field>
  
        <v-radio-group v-model="completed" label="Completed?">
          <v-radio label="Completed" value="1"></v-radio>
          <v-radio label="Did not complete" value="0"></v-radio>
        </v-radio-group>
  
        <v-text-field
          label="Route Setter"
          v-model="routeSetter"
          outlined
        ></v-text-field>
  
        <v-textarea label="Notes" v-model="notes" outlined></v-textarea>
  
        <v-row class="mt-4">
      <v-col cols="6">
        <v-btn @click="submitForm" block color="primary" large>
          Submit
        </v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn @click="clearForm" block color="secondary" large>
          Clear Form
        </v-btn>
      </v-col>
    </v-row>
      </v-container>
    </v-form>
  </template>
  
  <script>

  export default {
    data() {
      return {
        gym: "Vertical World: Seattle",
        date: "",
        givenGrade: "",
        gradeFeelsLike: "",
        grades: ["5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "5.10"],
        selectedStyle: "",
        numberValue: 0,
        completed: "",
        routeSetter: "",
        notes: "",
        };
    },
    methods: {
      submitForm() {
        // Here you can handle the form submission logic
        // For example, you can display an alert with the form data
        alert(`Name: ${this.gym}, Country: ${this.givenGrade}`);
      },
      clearForm() {
      // Set the form data properties to their initial values or clear them
      this.gym = '';
      this.selectedCountry = '';
      this.givenGrade = '';
      this.gradeFeelsLike = '';
      this.style = '';
      this.numberValue = '';
      this.completed = null; // or false, depending on your initial value
      this.setter = '';
      this.notes = '';
    },
    },
  };
  </script>
  
  <style>
/* Custom styles for the form */
.custom-container {
  max-width: 400px; /* Limit the width of the form */
  margin: auto; /* Center the form horizontally */
  padding: 20px; /* Add padding around the form */
  background-color: #f7f7f7; /* Set a background color */
  border-radius: 10px; /* Add rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Add a subtle box shadow */
}

/* Style the submit button */
.custom-container v-btn {
  margin-top: 20px; /* Add space between the form and the button */
}

/* Style the input fields */
.custom-container v-text-field,
.custom-container v-autocomplete,
.custom-container v-select,
.custom-container v-date-picker,
.custom-container v-radio-group,
.custom-container v-textarea {
  margin-bottom: 10px; /* Add space between the fields */
}
</style>