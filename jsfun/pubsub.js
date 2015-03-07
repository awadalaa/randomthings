var pubsub = (function(){
  var topics = {};
  return {
    subscribe: function(topic, listener) {
      if (!topics[topic]) topics[topic] = { queue: [] };
        var index = topics[topic].queue.push(listener) - 1;
        return (function(topic, index) {
          return {
            remove: function() {
         	  delete topics[topic].queue[index];
         	}
          }
       })(topic, index)
    },
    publish: function(topic, info) {
      // If the topic doesn't exist, or there's no listeners in queue, just leave
      if(!topics[topic] || !topics[topic].queue.length) return;
 
      // Cycle through topics queue, fire!
      var items = topics[topic].queue;
      for(var i = 0, len = items.length; i < len; i++) {
        if(typeof items[i] === 'function') items[i](info || {});
      }
    }
  };

})();