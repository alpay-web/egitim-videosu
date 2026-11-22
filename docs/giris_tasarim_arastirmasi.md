# Giriş kartı ve kapak tasarımı: 100 depo araştırması (2026-11)

**İstek:** girişteki yeşil kart her videoda aynıydı; her video farklı renk ve yazı tipiyle açılsın.

Hareketli grafik, kinetik tipografi, yazı tipi, renk paleti ve video giriş/kapak üreten 384 depo tarandı; 299'u
ilgili çıktı, en çok yıldızlı 100'ü aşağıda.

## Uygulananlar (`scripts/tema.py`)
| Fikir | Kaynak | Bizde |
|---|---|---|
| Hedef kontrasttan renk üretmek | adobe/leonardo (Apache) | alt yazı rengi WCAG ≥ 4.5 olana dek ayarlanır; başlık ≥ 7.6 |
| Uyumlu koyu/açık palet aileleri | radix-ui/colors, nordtheme/nord, catppuccin (MIT) | 15 tema: 12 koyu, 3 açık zemin |
| Açık kaynak yazı tipleri | google/fonts (OFL), ubuwaits/beautiful-web-type | Montserrat, Playfair, Sora, Poppins, Space Grotesk, DM Serif, Fraunces, Archivo Black, Outfit, Manrope, Merriweather, Bebas Neue, Work Sans, Lora, Nunito; hepsi Türkçe karakterli, ilk kullanımda indirilir |
| Yazı tipi metriğiyle dikey hizalama | seek-oss/capsize (MIT) | satır aralığı `getmetrics()` ile |
| Dengeli başlık satırları | shuding/react-wrap-balancer (MIT) | başlık "·" / "–" noktalarından bölünür, 3 satırı aşarsa küçülür |
| Kısa, ease-out giriş hareketi | LottieFiles/motion-design-skill, mojs (MIT) | kübik ease-out; 3 düzen: orta çizgi, sol dikey çizgi, köşe çerçevesi |

Seçim: senaryoda `"tema": 3` (sıra) veya `"tema": "bordo"` (ad); yoksa başlıktan türetilir. YouTube kapağı da aynı temayı kullanır.
BA serisinde video n → tema n.

## En çok yıldızlı 100 ilgili depo
| # | Depo | ★ | Lisans | Ne işe yarar |
|---|---|---|---|---|
| 1 | [nexu-io/open-design](https://github.com/nexu-io/open-design) | 108928 | Apache-2.0 | The 1st Collaborative AI Design Agent Workspace. Local-first and open source. Create motion, prototypes, websi |
| 2 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 88082 | Apache-2.0 | AI video you can actually edit. HyperFrames is a free, open-source AI video editor. Describe any video and get |
| 3 | [chenglou/pretext](https://github.com/chenglou/pretext) | 51088 | NOASSERTION | Fast, accurate & comprehensive text measurement & layout |
| 4 | [subframe7536/maple-font](https://github.com/subframe7536/maple-font) | 29843 | OFL-1.1 | Maple Mono: Open source monospace font with round corner, ligatures and Nerd-Font icons for IDE and terminal,  |
| 5 | [GraphiteEditor/Graphite](https://github.com/GraphiteEditor/Graphite) | 28006 | Apache-2.0 | Community-built comprehensive 2D content creation appplication for graphic design, digital art, and interactiv |
| 6 | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 22065 | Apache-2.0 | AI video skill for Claude Code & Codex — cinematic, editable product promos with Remotion: 124 shot recipe car |
| 7 | [catppuccin/catppuccin](https://github.com/catppuccin/catppuccin) | 19970 | MIT | 😸 Soothing pastel theme for the high-spirited! |
| 8 | [githubnext/monaspace](https://github.com/githubnext/monaspace) | 19844 | OFL-1.1 | An innovative superfamily of fonts for code |
| 9 | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 19747 | NOASSERTION | A toolbox of film styles made in code for Claude Code: 99 ready to use, and your own. Each style is a style pr |
| 10 | [mojs/mojs](https://github.com/mojs/mojs) | 18942 | MIT | The motion graphics toolbelt for the web |
| 11 | [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | 16195 | MIT | A growing collection of viral videos made with Claude Opus 5.5 and the prompts behind them. Watch each origina |
| 12 | [nexu-io/openmotion](https://github.com/nexu-io/openmotion) | 15041 | Apache-2.0 | The open-source Claude Motion & CapCut alternative. Turn a reference video into editable motion graphics with  |
| 13 | [theatre-js/theatre](https://github.com/theatre-js/theatre) | 13091 | Apache-2.0 | Motion design editor for the web |
| 14 | [mathjax/MathJax](https://github.com/mathjax/MathJax) | 10955 | Apache-2.0 | Beautiful and accessible math in all browsers |
| 15 | [chuspeeism/dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) | 10934 | AGPL-3.0 | An AI-agent skill that generates browser-editable presentations from multiple visual themes, exportable to HTM |
| 16 | [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) | 9185 | MIT | HTML PPT Studio — AgentSkill with 24 themes, 31 layouts, 20+ animations for building professional HTML present |
| 17 | [storytold/effectcraft](https://github.com/storytold/effectcraft) | 9115 | Apache-2.0 | EffectCraft: An open-source motion graphics and compositing tool written from scratch in pure Rust |
| 18 | [openfilm/openfilm](https://github.com/openfilm/openfilm) | 8962 | MIT | The open source AI video agent: turns any coding agent into a video agent, with editors to change anything it  |
| 19 | [rebassjs/rebass](https://github.com/rebassjs/rebass) | 7897 | MIT | :atom_symbol: React primitive UI components built with styled-system. |
| 20 | [styled-system/styled-system](https://github.com/styled-system/styled-system) | 7855 | MIT | ⬢ Style props for rapid UI development |
| 21 | [nolly-studio/cult-ui](https://github.com/nolly-studio/cult-ui) | 7618 | MIT | Animated components for design engineers. 150+ free shadcn/ui components, built with Tailwind CSS and Motion.  |
| 22 | [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 7447 | MIT | 艺术动画skill：35种艺术风格、9种解说语法，用代码让画动起来。 |
| 23 | [ubuwaits/beautiful-web-type](https://github.com/ubuwaits/beautiful-web-type) | 7348 | MIT | In-depth guide to the best open-source typefaces: https://www.beautifulwebtype.com |
| 24 | [nordtheme/nord](https://github.com/nordtheme/nord) | 6924 | MIT | An arctic, north-bluish color palette. |
| 25 | [sivan/heti](https://github.com/sivan/heti) | 6763 | MIT | 赫蹏（hètí）是专为中文内容展示设计的排版样式增强。它基于通行的中文排版规范而来，可以为网站的读者带来更好的文章阅读体验。 |
| 26 | [tailwindlabs/tailwindcss-typography](https://github.com/tailwindlabs/tailwindcss-typography) | 6490 | MIT | Beautiful typographic defaults for HTML you don't control. |
| 27 | [harfbuzz/harfbuzz](https://github.com/harfbuzz/harfbuzz) | 6243 | NOASSERTION | HarfBuzz text shaping engine |
| 28 | [system-ui/theme-ui](https://github.com/system-ui/theme-ui) | 5413 | MIT | Build consistent, themeable React apps based on constraint-based design principles |
| 29 | [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) | 5334 | MIT | An agent skill for building premium, immersive, scroll-driven websites. Works with Codex, Claude Code, and oth |
| 30 | [tixl3d/tixl](https://github.com/tixl3d/tixl) | 5197 | MIT | TiXL is an open source software to create realtime motion graphics. |
| 31 | [ant-design/ant-motion](https://github.com/ant-design/ant-motion) | 4632 | MIT |   :bicyclist: Animate specification and components of Ant Design |
| 32 | [simplefocus/FlowType.JS](https://github.com/simplefocus/FlowType.JS) | 4549 | MIT | Web typography at its finest: font-size and line-height based on element width. |
| 33 | [simonwep/pickr](https://github.com/simonwep/pickr) | 4495 | MIT | 🎨 Pickr - A simple, multi-themed, responsive and hackable Color-Picker library. No dependencies, no jQuery. Co |
| 34 | [feitangyuan/onetake](https://github.com/feitangyuan/onetake) | 4328 | NOASSERTION | Motion films that never cut to the next slide: every beat grows out of the one before, one continuous camera,  |
| 35 | [shuding/react-wrap-balancer](https://github.com/shuding/react-wrap-balancer) | 4216 | MIT | Simple React Component That Makes Titles More Readable |
| 36 | [alyssaxuu/motionity](https://github.com/alyssaxuu/motionity) | 4156 | MIT | The web-based motion graphics editor for everyone 📽 |
| 37 | [dembrandt/dembrandt](https://github.com/dembrandt/dembrandt) | 4054 | MIT | Extract any website’s design system into tokens in seconds: logo, colors, typography, borders & more. One comm |
| 38 | [scenario-labs/skills](https://github.com/scenario-labs/skills) | 3974 | MIT | Get production-ready images, video, audio, and 3D from any AI agent: skills that pick the right model, price b |
| 39 | [KyleAMathews/typography.js](https://github.com/KyleAMathews/typography.js) | 3856 | MIT | A powerful toolkit for building websites with beautiful design |
| 40 | [shinyobjectz/raea](https://github.com/shinyobjectz/raea) | 3851 | NOASSERTION | Render Anything Engine: tell your AI what to make. Videos, motion graphics, 3D and games as React and TypeScri |
| 41 | [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) | 3819 | MIT | 15 motion design styles, each made by Claude Opus 5.5 writing code from one prompt: watch the films, copy the  |
| 42 | [yanliudesign/mono-color-skill](https://github.com/yanliudesign/mono-color-skill) | 3713 | MIT | One-ink editorial print image skill — warm paper, halftone photography, active negative space, and restrained  |
| 43 | [hectahertz/react-native-typography](https://github.com/hectahertz/react-native-typography) | 3555 | MIT | Pixel–perfect, native–looking typographic styles for React Native ✒️ |
| 44 | [Rightpoint/BonMot](https://github.com/Rightpoint/BonMot) | 3543 | MIT | Beautiful, easy attributed strings in Swift |
| 45 | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | 3542 | MIT | Universal motion design principles for AI agents — timing, easing, choreography, and Disney animation principl |
| 46 | [Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | 3495 | NOASSERTION | Topic in, narrated explainer video out. A Claude Code / Codex skill that turns any topic into a black-canvas m |
| 47 | [Inkloom-art/inkloom](https://github.com/Inkloom-art/inkloom) | 3216 | NOASSERTION | Specialised AI models for logo design — a brand-analysis model turns a business into constraints, typography a |
| 48 | [alexmacarthur/typeit](https://github.com/alexmacarthur/typeit) | 3178 | GPL-3.0 | The most versatile JavaScript typewriter effect library on the planet. |
| 49 | [malcommac/SwiftRichString](https://github.com/malcommac/SwiftRichString) | 3140 | MIT | 👩‍🎨 Elegant Attributed String composition in Swift sauce |
| 50 | [dmtrKovalenko/fframes](https://github.com/dmtrKovalenko/fframes) | 3126 | MIT | programmatic video rendering framework that is actually fast |
| 51 | [bradley/Blotter](https://github.com/bradley/Blotter) | 3082 | NOASSERTION | A JavaScript API for drawing unconventional text effects on the web. |
| 52 | [allweonedev/presentation-ai](https://github.com/allweonedev/presentation-ai) | 3082 | MIT | ALLWEONE® Open source AI presentation generator Gamma Alternative. Create professional slides with customizabl |
| 53 | [bennyguitar/Colours](https://github.com/bennyguitar/Colours) | 3079 | MIT | A beautiful set of predefined colors and a set of color methods to make your iOS/OSX development life easier. |
| 54 | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | 3066 | NOASSERTION | Herk Edit Kit by Nate Herk: edit videos, reels, and YouTube Shorts with Codex or Claude Code. 15 skills, trans |
| 55 | [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) | 3018 | MIT | Turn one topic into a finished Vox-style paper-collage explainer/ad video — automated end to end on Atlas Clou |
| 56 | [alchaincyf/huashu-motion](https://github.com/alchaincyf/huashu-motion) | 2976 | MIT | 让你的agent一键直出商业级产品宣传片：会作曲，能指着画面改。Commercial-grade launch films by your coding agent — point at the frame to cha |
| 57 | [bangtutorial/bang-motion](https://github.com/bangtutorial/bang-motion) | 2916 | MIT | Agent skill for browser motion graphics — openers, promos, bumpers, kinetic typography, and five explainer sty |
| 58 | [matejlatin/Gutenberg](https://github.com/matejlatin/Gutenberg) | 2843 | NOASSERTION | A meaningful web typography starter kit. |
| 59 | [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | 2536 | NOASSERTION | Open-source skills and toolkits that let Claude Code, Codex and other coding agents make video. 180 repos by t |
| 60 | [hanzipro/han.css](https://github.com/hanzipro/han.css) | 2525 | MIT | 「漢字標準格式」印刷品般的漢字排版框架 Han.css: the CSS typography framework optimised for Hanzi. |
| 61 | [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | 2478 | NOASSERTION | Agent skill that turns Claude Code / Codex into a motion-design studio for voiceover-driven explainer videos — |
| 62 | [JacquesLucke/animation_nodes](https://github.com/JacquesLucke/animation_nodes) | 2396 | NOASSERTION | Node based visual scripting system designed for motion graphics in Blender. |
| 63 | [Achno/gowall](https://github.com/Achno/gowall) | 2333 | MIT | A tool to convert a Wallpaper's color scheme / palette, OCR with VLM's Traditional & Hybrid, Image Compression |
| 64 | [color-js/color.js](https://github.com/color-js/color.js) | 2328 | MIT | Color conversion & manipulation library by the editors of the CSS Color specifications |
| 65 | [cth9191/animate](https://github.com/cth9191/animate) | 2199 | MIT | Procedural animation in any style for Claude Code: short single-file canvas videos with story, look and storyb |
| 66 | [adobe/leonardo](https://github.com/adobe/leonardo) | 2189 | Apache-2.0 | Generate colors based on a desired contrast ratio |
| 67 | [karthik/wesanderson](https://github.com/karthik/wesanderson) | 2176 | NOASSERTION | A Wes Anderson color palette for R |
| 68 | [EverettFish/holo-card-studio](https://github.com/EverettFish/holo-card-studio) | 2131 | NOASSERTION | Turn the user's description or uploaded reference into a finished, editable Blender card and an interactive Th |
| 69 | [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) | 2102 | MIT | Open-source AI video style cloning for 2D animation. Give it a reference video or YouTube link; Claude Code or |
| 70 | [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | 2027 | MIT | 56 open-source skills that teach your AI coding agent to make motion graphics, animation & video — kinetic typ |
| 71 | [astrofox-io/astrofox](https://github.com/astrofox-io/astrofox) | 2026 | MIT | Astrofox is a motion graphics program that lets you turn audio into stunning visuals. |
| 72 | [rbanffy/3270font](https://github.com/rbanffy/3270font) | 2022 | NOASSERTION | A 3270 font in a modern format |
| 73 | [onblog/miaomiao-bar](https://github.com/onblog/miaomiao-bar) | 1967 | AGPL-3.0 | A macOS clipboard workbench: text and pictures that land on the clipboard leave usable. 喵喵剪贴板：macOS 上的剪贴板工作台，文 |
| 74 | [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) | 1942 | Apache-2.0 | Art and animation, written as code. Illustrations, loops, interactive web art, launch-videos and scored films  |
| 75 | [SonyWWS/ATF](https://github.com/SonyWWS/ATF) | 1924 | Apache-2.0 | Authoring Tools Framework (ATF) is a set of C#/.NET components for making tools on Windows. ATF has been in co |
| 76 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | 1849 | Apache-2.0 | Open-source, agent-driven editing pipeline: create subtitles, motion graphics, slides, edit and render videos. |
| 77 | [braver/programmingfonts](https://github.com/braver/programmingfonts) | 1848 | MIT | Test drive programming fonts online: the definitive list of fonts for code. |
| 78 | [WebPraktikos/universal-resume](https://github.com/WebPraktikos/universal-resume) | 1807 | NOASSERTION | Minimal and formal résumé (CV) website template for print, mobile, and desktop. |
| 79 | [Ebony-Vinyl/EAC-design-world](https://github.com/Ebony-Vinyl/EAC-design-world) | 1806 | AGPL-3.0 | DeepSeek Harness 本地视频制作与设计插件：多轨剪辑、模板与设计体系、原生预览画布和真实文件导出 |
| 80 | [devinhunt/typebase.css](https://github.com/devinhunt/typebase.css) | 1795 | MIT | A starting point for good typography on the web. |
| 81 | [aagarwal1012/Animated-Text-Kit](https://github.com/aagarwal1012/Animated-Text-Kit) | 1773 | MIT | 🔔  A flutter package to create cool and beautiful text animations. [Flutter Favorite Package] |
| 82 | [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | 1765 | Apache-2.0 | Looksmaxxing for motion graphics. An agent skill that turns AI slop videos into films that look made by a moti |
| 83 | [radix-ui/colors](https://github.com/radix-ui/colors) | 1748 | MIT | A gorgeous, accessible color system. |
| 84 | [BalazsJako/ImGuiColorTextEdit](https://github.com/BalazsJako/ImGuiColorTextEdit) | 1741 | MIT | Colorizing text editor for ImGui |
| 85 | [seek-oss/capsize](https://github.com/seek-oss/capsize) | 1735 | MIT | Flipping how we define typography in CSS. |
| 86 | [cormullion/juliamono](https://github.com/cormullion/juliamono) | 1711 | OFL-1.1 | JuliaMono is a monospaced font for scientific and technical users, with comprehensive Unicode support. |
| 87 | [kevinraymond/florilegium](https://github.com/kevinraymond/florilegium) | 1692 | MIT | Procedurally generated Delft-blue page margins for LuaLaTeX, with plants, visitors, shells and Gothic tracery  |
| 88 | [LingDong-/qiji-font](https://github.com/LingDong-/qiji-font) | 1682 | OFL-1.1 | 齊伋體 - typeface from Ming Dynasty woodblock printed books |
| 89 | [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) | 1629 | MIT | A motion design skill with two modes — build interactive components with purposeful motion, or audit existing  |
| 90 | [Fenng/Tech-Doc-Style-Chinese](https://github.com/Fenng/Tech-Doc-Style-Chinese) | 1605 | MIT | Yet another reusable writing skill for Chinese technical documentation and product copy. |
| 91 | [lochie/torph](https://github.com/lochie/torph) | 1570 | MIT | Dependency-free animated text component. |
| 92 | [yamlresume/yamlresume](https://github.com/yamlresume/yamlresume) | 1563 | MIT | Resumes as code in YAML, brought to you with ❤️ by PPResume. |
| 93 | [Jolg42/awesome-typography](https://github.com/Jolg42/awesome-typography) | 1554 | CC0-1.0 | ✏︎ Curated list about digital typography 🔥 |
| 94 | [HeyChengC/vibe-knowledge-film](https://github.com/HeyChengC/vibe-knowledge-film) | 1496 | NOASSERTION | 抖音爆款Vibe知识大赏知识短片skill，深度拆解爆款视频，复刻画风，导演分镜表，自动配音效，一键出片 |
| 95 | [hendurhance/ui-ux](https://github.com/hendurhance/ui-ux) | 1469 | CC0-1.0 | 📚 This guide is designed to help you learn UI/UX design, and is divided into three levels: Beginner, Intermedi |
| 96 | [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) | 1443 | MIT | Claude Code skill kit for premium AI-assisted business videos: independent critic loop, motion principles from |
| 97 | [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) | 1439 | NOASSERTION | Motion-graphics skills for Claude Code and Codex. |
| 98 | [Leonxlnx/cinetic](https://github.com/Leonxlnx/cinetic) | 1351 | MIT | Cinematic launch films and motion design from code, directed by your coding agent. |
| 99 | [NeverCease/uchu](https://github.com/NeverCease/uchu) | 1344 | Unlicense | → https://code.webb.page/nevercease/uchu.git |
| 100 | [Siddharth11/Colorful](https://github.com/Siddharth11/Colorful) | 1331 | CC0-1.0 | A curated list of awesome resources to choose your next color scheme |