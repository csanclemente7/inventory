<template>
  <main class="login">
    <!-- SECTION LOGIN HEADER -->
    <section class="login__header">
      <img
        src="../assets/img/Logo_macris_blanco.png"
        alt=""
        class="login__img"
      />
      <h2 class="login__title">Inventario</h2>
      <h1 class="login__subtitle">Inicio de Sesión</h1>
    </section>

    <!-- SECTION LOGIN FORM -->
    <form v-on:submit.prevent="processLogInUser" class="login__form">
      <div class="login__item">
        <span class="login__text">Correo Electrónico</span>
        <i class="fas fa-envelope"></i>
        <input
          class="login__input"
          type="email"
          v-model="user.email"
          id="email"
          name="email"
          placeholder="correo"
          required
        />
      </div>
      <div class="login__item">
        <span class="login__text">Contraseña</span>
        <i class="fas fa-lock"></i>
        <input
          class="login__input"
          type="password"
          v-model="user.password"
          name="password"
          id="password"
          placeholder="contraseña"
          required
        />
      </div>
      <div class="login__errors">
        <i
          class="fa fa-exclamation-circle"
          id="error-icon"
          v-if="errorAuth"
        ></i>
        <span v-if="error_message" class="login__text text_fail">{{
          " " + error_message
        }}</span>
      </div>
      <button type="submit" class="login__submit">Iniciar Sesión</button>
      <!--<a href="#" class="login__link">¿Olvidaste tu contraseña?</a>-->
    </form>

    <!-- ANIMATED BACKGROUND -->
    <ul class="bg-bubbles">
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
      <li></li>
    </ul>
  </main>

  <!-- LOADER -->
  <div class="lds-spinner" v-if="startLogin">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LogIn",
  data: function () {
    return {
      user: {
        email: "",
        password: "",
      },
      error_message: "",
      errorAuth: false,
      startLogin: false,
    };
  },
  methods: {
    processLogInUser: function () {
      this.startLogin = true;
      axios
        .post("https://inventory-bk.herokuapp.com/login", this.user, {
          headers: {},
        })
        .then((result) => {
          let dataLogIn = {
            email: this.user.email,
            token_access: result.data.access,
            token_refresh: result.data.refresh,
          };
          this.startLogin = false;
          this.$emit("completedLogIn", dataLogIn);
        })
        .catch((error) => {
          if (error.response.status == "401")
            this.error_message = "Correo o contraseña incorrectos";
          this.errorAuth = true;
          this.startLogin = false;
        });
    },
  },
};
</script>

<style>
/* import css from assets local folder */

@import "../assets/css/login/login.css";
@import "../assets/css/login/login-header.css";
@import "../assets/css/login/login-form.css";
/* bg-bubbles */
@import "../assets/css/common/bg-bubbles.css";
</style>
