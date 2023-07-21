<!-- <template>
  <router-view />
  <v-app>
    <v-container>
      <HardcodedForm />
    </v-container>
  </v-app>
</template> -->

<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        expand-on-hover
        rail
      >
        <v-list>
          <v-list-item
            prepend-avatar=""
            title="Jessica Dyer"
            subtitle="sandra_a88@gmailcom"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="Shared with me" value="shared"></v-list-item>
          <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <v-container>
      <HardcodedForm />
    </v-container>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script>
import HardcodedForm from "./components/HardcodedForm.vue";

export default {
  components: {
    HardcodedForm,
  },
};
</script>
