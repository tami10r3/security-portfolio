/* ===========================================================
   Ambient network background.
   Nodes drift slowly; the cursor gently repels nearby nodes and
   draws connecting lines to them, like it's part of the graph.
   Respects prefers-reduced-motion (canvas is display:none via CSS,
   this script also exits early so no work is done).
   =========================================================== */

(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) return;

  var canvas = document.createElement("canvas");
  canvas.id = "bg-canvas";
  var glow = document.createElement("div");
  glow.id = "bg-glow";
  document.body.insertBefore(glow, document.body.firstChild);
  document.body.insertBefore(canvas, document.body.firstChild);

  var ctx = canvas.getContext("2d");
  var W, H, DPR;
  var nodes = [];
  var mouse = { x: null, y: null, active: false };

  var NODE_COUNT_DENSITY = 22000; // px^2 per node, lower = denser
  var LINK_DIST = 130;
  var MOUSE_DIST = 160;
  var MOUSE_LINK_DIST = 200;

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * DPR;
    canvas.height = H * DPR;
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    initNodes();
  }

  function initNodes() {
    var count = Math.max(18, Math.min(60, Math.floor((W * H) / NODE_COUNT_DENSITY)));
    nodes = [];
    for (var i = 0; i < count; i++) {
      nodes.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.15,
        vy: (Math.random() - 0.5) * 0.15,
        r: 1.2 + Math.random() * 1.1
      });
    }
  }

  function step() {
    ctx.clearRect(0, 0, W, H);

    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];

      // gentle drift
      n.x += n.vx;
      n.y += n.vy;

      // wrap around edges
      if (n.x < -20) n.x = W + 20;
      if (n.x > W + 20) n.x = -20;
      if (n.y < -20) n.y = H + 20;
      if (n.y > H + 20) n.y = -20;

      // soft repel from cursor
      if (mouse.active) {
        var dx = n.x - mouse.x;
        var dy = n.y - mouse.y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MOUSE_DIST && dist > 0.01) {
          var force = (1 - dist / MOUSE_DIST) * 0.6;
          n.x += (dx / dist) * force;
          n.y += (dy / dist) * force;
        }
      }
    }

    // draw links between nearby nodes
    ctx.lineWidth = 1;
    for (var a = 0; a < nodes.length; a++) {
      for (var b = a + 1; b < nodes.length; b++) {
        var dx2 = nodes[a].x - nodes[b].x;
        var dy2 = nodes[a].y - nodes[b].y;
        var d = Math.sqrt(dx2 * dx2 + dy2 * dy2);
        if (d < LINK_DIST) {
          var alpha = (1 - d / LINK_DIST) * 0.16;
          ctx.strokeStyle = "rgba(76, 159, 232, " + alpha + ")";
          ctx.beginPath();
          ctx.moveTo(nodes[a].x, nodes[a].y);
          ctx.lineTo(nodes[b].x, nodes[b].y);
          ctx.stroke();
        }
      }

      // link node to cursor if close, cursor acts like a node in the graph
      if (mouse.active) {
        var dxm = nodes[a].x - mouse.x;
        var dym = nodes[a].y - mouse.y;
        var dm = Math.sqrt(dxm * dxm + dym * dym);
        if (dm < MOUSE_LINK_DIST) {
          var alphaM = (1 - dm / MOUSE_LINK_DIST) * 0.28;
          ctx.strokeStyle = "rgba(76, 159, 232, " + alphaM + ")";
          ctx.beginPath();
          ctx.moveTo(nodes[a].x, nodes[a].y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();
        }
      }
    }

    // draw nodes
    for (var c = 0; c < nodes.length; c++) {
      var nd = nodes[c];
      ctx.beginPath();
      ctx.arc(nd.x, nd.y, nd.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(124, 135, 151, 0.5)";
      ctx.fill();
    }

    requestAnimationFrame(step);
  }

  window.addEventListener("resize", resize);
  window.addEventListener("mousemove", function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
    document.documentElement.style.setProperty("--mx", e.clientX + "px");
    document.documentElement.style.setProperty("--my", e.clientY + "px");
  });
  window.addEventListener("mouseleave", function () {
    mouse.active = false;
  });

  resize();
  requestAnimationFrame(step);
})();
