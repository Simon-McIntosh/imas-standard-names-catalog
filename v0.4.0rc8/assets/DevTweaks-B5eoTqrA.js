import{r as l,j as e}from"./vendor-react-DuOeAc5B.js";const v=`
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    background:rgba(250,249,247,.88);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;
    padding:10px 8px 10px 14px;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);
    width:22px;height:22px;border-radius:6px;cursor:pointer;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;
    overflow-y:auto;min-height:0}
  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-row-h{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;
    color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;
    background:rgba(0,0,0,.06);user-select:none}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;
    background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;
    border-radius:6px;cursor:pointer;padding:4px 6px;line-height:1.2}
  .twk-seg button.on{background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12)}
  .twk-chips{display:flex;gap:6px}
  .twk-chip{position:relative;appearance:none;flex:1;min-width:0;height:46px;
    padding:0;border:0;border-radius:6px;overflow:hidden;cursor:pointer;
    box-shadow:0 0 0 .5px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.06);
    transition:transform .12s cubic-bezier(.3,.7,.4,1),box-shadow .12s}
  .twk-chip:hover{transform:translateY(-1px)}
  .twk-chip[data-on="1"]{box-shadow:0 0 0 1.5px rgba(0,0,0,.85),0 2px 6px rgba(0,0,0,.15)}
`;function c({label:r,children:a}){return e.jsxs(e.Fragment,{children:[e.jsx("div",{className:"twk-sect",children:r}),a]})}function p({label:r,value:a,options:s,onChange:i}){const t=s.map(n=>typeof n=="object"?n:{value:n,label:n});return e.jsxs("div",{className:"twk-row",children:[e.jsx("div",{className:"twk-lbl",children:e.jsx("span",{children:r})}),e.jsx("div",{className:"twk-seg",role:"radiogroup",children:t.map(n=>e.jsx("button",{type:"button",role:"radio","aria-checked":n.value===a,className:n.value===a?"on":"",onClick:()=>i(n.value),children:n.label},n.value))})]})}function y({label:r,value:a,options:s,onChange:i}){return e.jsxs("div",{className:"twk-row",children:[e.jsx("div",{className:"twk-lbl",children:e.jsx("span",{children:r})}),e.jsx("div",{className:"twk-chips",role:"radiogroup",children:s.map(t=>e.jsx("button",{type:"button",role:"radio","aria-checked":t===a,"data-on":t===a?"1":"0",className:"twk-chip",style:{background:t},title:t,onClick:()=>i(t),"aria-label":t},t))})]})}function N({tweaks:r,setTweak:a}){const[s,i]=l.useState(!0),t=l.useRef(null),[n,h]=l.useState({x:16,y:16});l.useEffect(()=>{t.current&&(t.current.style.right=n.x+"px",t.current.style.bottom=n.y+"px")},[n]);const g=o=>{if(!t.current)return;const d=t.current.getBoundingClientRect(),w=o.clientX,m=o.clientY,f=window.innerWidth-d.right,k=window.innerHeight-d.bottom,x=b=>{h({x:Math.max(8,f-(b.clientX-w)),y:Math.max(8,k-(b.clientY-m))})},u=()=>{window.removeEventListener("mousemove",x),window.removeEventListener("mouseup",u)};window.addEventListener("mousemove",x),window.addEventListener("mouseup",u)};return s?e.jsxs(e.Fragment,{children:[e.jsx("style",{children:v}),e.jsxs("div",{ref:t,className:"twk-panel",children:[e.jsxs("div",{className:"twk-hd",onMouseDown:g,style:{cursor:"move"},children:[e.jsx("b",{children:"Tweaks"}),e.jsx("button",{className:"twk-x",onClick:()=>i(!1),children:"✕"})]}),e.jsxs("div",{className:"twk-body",children:[e.jsx(c,{label:"Density",children:e.jsx(p,{label:"List rows",value:r.density,options:[{value:"comfortable",label:"Comfy"},{value:"compact",label:"Compact"},{value:"dense",label:"Dense"}],onChange:o=>a("density",o)})}),e.jsx(c,{label:"Layout",children:e.jsx(p,{label:"Group results",value:r.groupBy,options:[{value:"none",label:"A–Z"},{value:"category",label:"Domain"},{value:"cluster",label:"Concept"}],onChange:o=>a("groupBy",o)})}),e.jsxs(c,{label:"Theme",children:[e.jsx(p,{label:"Mode",value:r.theme,options:[{value:"light",label:"Light"},{value:"dark",label:"Dark"}],onChange:o=>a("theme",o)}),e.jsx(y,{label:"Accent",value:r.accent,options:["#3654c8","#0d7c66","#a8430d","#7a3aa8","#1d2230"],onChange:o=>a("accent",o)})]})]})]})]}):null}export{N as default};
//# sourceMappingURL=DevTweaks-B5eoTqrA.js.map
