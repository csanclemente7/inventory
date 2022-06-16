<template>
  <div class="home">
    <div class="home-data">
      <div class="button-container">
        <button v-on:click="openPopUp('exit')" class="button red">
          <img src="../assets/img/exit.png" />
        </button>

        <button v-on:click="openPopUp('entry')" class="button green">
          <img src="../assets/img/entry.png" alt="" />
        </button>
      </div>
      <div class="image">
        <img src="../assets/img/home_image.svg" alt="" />
        <h3>Todo al día</h3>
      </div>
    </div>
  </div>
  <!--- POP UP EXIT -->
  <section class="popups_container">
    <div class="popup" v-if="popUps.exit">
      <div class="popup-close-container">
        <div class="popup_close" v-on:click="closePopUp('item')">
          <svg
            width="25"
            height="25"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="var(--link-red-light)"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </div>
      </div>

      <div class="create-report__errors">
        <i
          class="fa fa-exclamation-circle"
          id="error-icon"
          v-if="errors.error_message"
        ></i>
        <span v-if="!errors.error_createQuotation" class="text_success">{{
          " " + success_message
        }}</span>
        <span v-if="errors.error_createQuotation" class="text_fail">{{
          " " + errors.error_message
        }}</span>
      </div>

      <h1 class="popup_title">
        <img src="../assets/img/quotation_img.png" alt="" />&nbsp; Agregar
        insumos
      </h1>

      <!--- Form -->
      <form
        class="formulario item-create-form"
        v-on:submit.prevent="processCreateItem"
      >
        <div class="header-form">
          <div class="input-container name">
            <input
              type="text"
              name="name"
              id="name"
              class="input"
              v-model="item.name"
              maxlength="70"
              autocomplete="off"
              required
            />
            <label class="input-label" for="price">Item</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>
          <div class="input-container price">
            <input
              type="text"
              name="price"
              id="price"
              class="input"
              v-model="item.price"
              maxlength="30"
              autocomplete="off"
              required
            />
            <label class="input-label" for="price">Precio</label>
            <span class="input-message-error">Este campo no es valido</span>
          </div>

          <div class="input-container">
            <button class="button" type="submit">Agregar</button>
          </div>
        </div>
      </form>

      <!-- TABLE -->
      <table class="custom-responsiva-two">
        <thead>
          <tr>
            <th>Item</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody>
          <!--- problema a resolver -->
          <tr
            v-for="item in paginatedData"
            :key="item"
            id="table_row delete-custom"
          >
            <td v-on:click="openPopUpItemUpdate('itemUpdate', item)">
              {{ item.name }}
            </td>
            <td v-on:click="openPopUpItemUpdate('itemUpdate', item)">
              ${{ priceToString(item.price) }}
            </td>
            <!-- delete button -->
            <td>
              <button
                class="delete-button"
                type="button"
                aria-label="submit form"
                v-on:click="processDeleteItemUpdate(items, item)"
              >
                <!-- delete icon -->
                <li class="fa fa-trash"></li>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  name: "Home",
  data: function () {
    return {
      popUps: {
        exit: false,
        entry: false,
        item: false,
      },
    };
  },
  openPopUp: function (popUp) {
    //this.home = document.querySelector(".home");
    //this.home.classList.add("parentDiv");
    this.popUps[popUp] = true;
  },

  closePopUp: function (popUp) {
    this.popUps[popUp] = false;
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-data image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.image img {
  width: 30%;
  height: auto;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
@import "../assets/css/common/popUp.css";
@import "../assets/css/common/grid-menu.css";
@import "../assets/css/common/inputs.css";
@import "../assets/css/common/button.css";
@import "../assets/css/common/links.css";
@import "../assets/css/common/suggestion.css";
@import "../assets/css/base/base.css";
@import "../assets/css/common/table.css";
@import "../assets/css/common/tableResults.css";
@import "../assets/css/common/lds-ripple.css";
</style>
