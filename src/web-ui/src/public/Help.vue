<template>
  <Layout>
    <div class="content">
      <div class="container">
        <h3>Customer Support</h3>

        <!-- Checking backend indicator -->
        <div class="container mb-4" v-if="checkingBackend">
          <i class="fas fa-spinner fa-spin fa-3x"></i>
        </div>

        <!-- Backend configured -->
        <div v-if="backendConfigured">
          <p>Support available 24/7/365. For immediate assistance please ask a question using the form below and our virtual assistant will direct your request.
          </p>
          <div class="row">
            <div class="col-sm">
              <Chatbot @chatResponse="handleChatResponse" v-bind:chatbotConfig="chatbotConfig" id="chatBot"></Chatbot>
            </div>
            <div class="col-sm">
              <div class="card-deck">
                <div class="card card-recommend mb-3" v-for="card in responseCards" v-bind:key="card.title">
                  <img class="card-img-top" :src="card.imageUrl" :alt="card.title" />
                  <div class="card-body">
                    <h6 class="card-title">{{ card.title }}</h6>
                    <p class="card-text"><small>{{ card.subTitle }}</small></p>
                    <a class="btn btn-secondary btn-block mt-auto" :href="card.attachmentLinkUrl">Learn more...</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Backend NOT configured -->
        <div v-if="!checkingBackend && !backendConfigured">
          <p>The virtual assistant does not appear to be configured for this deployment.
          </p>
        </div>

        <div v-if="error" class="error">
          {{ error }}
        </div>

      </div>
    </div>
  </Layout>
</template>

<script>
import { Interactions as InteractionsLexV1 } from '@aws-amplify/interactions/lex-v1';

import Layout from '@/components/Layout/Layout.vue'
import Chatbot from '@/components/Chatbot.vue'

export default {
  name: 'Help',
  components: {
    Layout,Chatbot
  },
  data () {
    return {
      checkingBackend: false,
      backendConfigured: null,
      error: null,
      responseCards: null
    }
  },
  created () {
    this.checkBackend()
  },
  methods: {
    async checkBackend() {
      this.checkingBackend = true

      try {
        await InteractionsLexV1.send({ botName: this.chatbotConfig.bot, message: 'Hey Retail Demo Store' });
        this.backendConfigured = true
      }
      catch(err) {
        console.error('Error communicating with chatbot: ' + err)
        this.error = err
        this.backendConfigured = false
      }
      finally {
        this.checkingBackend = false
      }
    },
    async handleChatResponse(response) {
      var botCtr = document.getElementById('chatBot');
      botCtr.scrollTop = botCtr.scrollHeight;
      if (response.responseCard && response.responseCard.genericAttachments) {
        this.responseCards = response.responseCard.genericAttachments
      }
      else {
        this.responseCards = null
      }
    }
  },
  computed: {
    chatbotConfig: function () {
      let config = {
        bot: import.meta.env.VITE_BOT_NAME,
        clearComplete: false,
        botTitle: "Retail Demo Store Support",
        conversationModeOn: false,
        voiceEnabled: false,
        textEnabled: true
      }
      return config
    }
  },
}
</script>

<style scoped>
  #chatBot {
    margin-top: 0px;
    max-height: 95vh;
    overflow-y: auto;
  }

  .card-recommend {
    min-width: 250px;
  }

  .error {
    margin-bottom: 150px;
  }
</style>