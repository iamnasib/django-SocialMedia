console.log(`{{stories|safe}}`)
let stories = new Zuck(`{{stories}}`, {
    skin: 'snapgram',      // container class
    avatars: true,         // shows user photo instead of last story item preview
    list: false,           // displays a timeline instead of carousel
    openEffect: true,      // enables effect when opening story
    cubeEffect: false,     // enables the 3d cube effect when sliding story
    autoFullScreen: false, // enables fullscreen on mobile browsers
    backButton: true,      // adds a back button to close the story viewer
    backNative: false,     // uses window history to enable back button on browsers/android
    previousTap: true,     // use 1/3 of the screen to navigate to previous item when tap the story
    localStorage: true,    // set true to save "seen" position. Element must have a id to save properly.
    reactive: true,        // set true if you use frameworks like React to control the timeline (see react.sample.html)
    rtl: false,            // enable/disable RTL
  
    stories: [ // array of stories
      // see stories structure example
    ],
  
    callbacks:  {
      onOpen (storyId, callback) {
        callback();  // on open story viewer
      },
  
      onView (storyId) {
        // on view story
      },
  
      onEnd (storyId, callback) {
        callback();  // on end story
      },
  
      onClose (storyId, callback) {
        callback();  // on close story viewer
      },
  
      onNavigateItem (storyId, nextStoryId, callback) {
        callback();  // on navigate item of story
      },
  
      onDataUpdate (currentState, callback) {
        callback(); // use to update state on your reactive framework
      }
    },
  
    template: {
      // use these functions to render custom templates
      // see src/zuck.js for more details
  
      timelineItem (itemData) {
        return ``;
      },
  
      timelineStoryItem (itemData) {
        return ``;
      },
  
      viewerItem (storyData, currentStoryItem) {
        return ``;
      },
  
      viewerItemPointer (index, currentIndex, item) {
        return ``;
      },
  
      viewerItemBody (index, currentIndex, item) {
        return ``;
      }
    },
  
    language: { // if you need to translate :)
      unmute: 'Touch to unmute',
      keyboardTip: 'Press space to see next',
      visitLink: 'Visit link',
      time: {
        ago:'ago', 
        hour:'hour', 
        hours:'hours', 
        minute:'minute', 
        minutes:'minutes', 
        fromnow: 'from now', 
        seconds:'seconds', 
        yesterday: 'yesterday', 
        tomorrow: 'tomorrow', 
        days:'days'
      }
    }
  });