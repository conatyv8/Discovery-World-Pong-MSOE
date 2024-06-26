console.log("depth feed viewer:")

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("Connected to MQTT broker");
    client.subscribe("depth/feed");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

function myMethod(message) {
    if (message.destinationName === "depth/feed") {
        // console.log('received depth image')
        last_depth = (JSON.parse(message.payloadString)["feed"])
        requestAnimationFrame(render_loop)
        //console.log(depthFeedStr)
        //decoded = atob(rawfeed)
    }
}

// https://stackoverflow.com/a/23105310
// Draw image scaled to the screen and centered
function drawImageScaled(img, ctx) {
   var canvas = ctx.canvas ;
   var hRatio = canvas.width  / img.width    ;
   var vRatio =  canvas.height / img.height  ;
   var ratio  = Math.min ( hRatio, vRatio );
   var centerShift_x = ( canvas.width - img.width*ratio ) / 2;
   var centerShift_y = ( canvas.height - img.height*ratio ) / 2;  
   ctx.clearRect(0,0,canvas.width, canvas.height);
   ctx.drawImage(img, 0,0, img.width, img.height,
                      centerShift_x,centerShift_y,img.width*ratio, img.height*ratio);  
}

function render_depth_feed(ctx, image_upscale = 3.6) {
    var image = new Image();
    image.src = 'data:image/jpg;base64,' + last_depth

    // You have to use image.onload so that you dont try to use the image before it exists
    image.onload = function () {
	drawImageScaled(image, ctx);
    }


}

function init() {
    /*
    Basic housekeeping initialization. Makes sure the canvases we need
    exist, and do any precomputing or sizing that aren't model dependent.
    */
    // Create a client instance
    client = new Paho.Client("localhost", 9001, "human-visualizer");

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = myMethod; // onMessageArrived;

    // connect the client
    client.connect({onSuccess:onConnect, reconnect:true});

    // canvas for our depth camera image
    d_canvas = document.getElementById("depth");
    const d_ctx = d_canvas.getContext("2d");

    // A listener to appropriately resize our canvases when the window size changes
    // window.addEventListener('resize', onWindowResizeV, false);

    initialized = true;
}
 
function render_loop() {
    if(last_depth && last_depth != last_rendered_depth) {
        const depth_ctx = d_canvas.getContext('2d')
        render_depth_feed(depth_ctx)
        last_rendered_depth = last_depth
    }

    requestAnimationFrame(render_loop)
}

//placeholder
var last_depth = "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";
var last_rendered_depth = ""

// canvas for our depth camera image
d_canvas = document.getElementById("depth");
const d_ctx = d_canvas.getContext("2d");

render_depth_feed(d_ctx)

window.onload = init
