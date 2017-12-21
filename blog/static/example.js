// Example of change method with a failure closure
// This structure can be used in any methods of Pressure
// The failure block will return with an "error" and message showing why the device doesn't support 3D Touch and Force Touch

$.pressureConfig({
  polyfill: false
});

var block = {
  start: function(event){
    console.log('start', event);
  },

  change: function(force, event){
    // event.preventDefault();
    console.log('change', force);
    var canvas = document.getElementsByClassName("drawing-board-canvas")[0];
    canvas.getContext("2d").lineWidth = force*2;
  },

  startDeepPress: function(event){
    console.log('start deep press', event);
  },

  endDeepPress: function(){
    console.log('end deep press');
  },

  end: function(){
    console.log('end');
  },

  unsupported: function(){
    console.log(this);
    this.innerHTML = 'Your device / browser does not support this :(';
  }
}

Pressure.set(document.querySelectorAll('#el1'), block);
Pressure.set(document.querySelectorAll(".drawing-board-canvas"), block);

$('#el1-jquery').pressure(block);



