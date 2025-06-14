[![3OtOp7R.th.png](https://iili.io/3OtOp7R.th.png)](https://freeimage.host/i/3OtOp7R)

# Cursor Enhancer for Cursor IDE ✨

**Cursor** would often call it quits way too early! I'd give it a complex task, it'd use maybe 5 of
its ~25 available tool calls for that single "main request," then call it a day. Not only was that
untapped AI power for that _single thought_, but making small follow-up tweaks meant starting a _new
request_. Doing that too often, and my precious **~500 monthly requests** (you know the ones!) would
burn up much faster than I liked :(

**Presenting: The Cursor Enhancer – The "Turn Your 500 Cursor Requests into 2500!" Rule with
Interactive Popups & Visual Context!** (Okay, maybe not _always_ a perfect 5x, but you get the damn
idea! 😉)

I evolved this Global Rule for our beloved Cursor IDE to transform my (and your!) AI from a quick
sprinter into an endurance marathon runner for complex ideas, all within the lifecycle of a _single
main request_. Now it's **supercharged with image uploads and a beautiful popup interface!** I've
basically told Cursor: "Hold up, _we're_ not done with this request until _I_ say we're done."
Before it dares to end the conversation, it _must_ open a special **interactive popup** for my (and
your!) final, iterative commands with visual context support.

If each main request can now handle the depth of what might have taken 5 separate (and shallow)
requests before, we're effectively **supercharging those ~500 monthly requests to feel like 2500 in
terms of iterative power!** It's about making every single one count, HARD.

## 🎬 Quick Demo:

**See Cursor Enhancer in action!** → https://www.youtube.com/watch?v=mZmNM-AIf4M

## ✨ Key Awesomeness (What Cursor Enhancer Packs In)

- **📷 Visual Context Sharing:** Upload images, screenshots, diagrams, or mockups directly in the
  popup. The AI sees everything you share.
- **🎨 Beautiful Popup Interface:** Professional orange-glow design that fits perfectly in Cursor
  with real-time MCP status indicators.
- **AI On MY Leash:** Makes the Cursor Agent wait for _my_ (and your!) "go-ahead" via an interactive
  popup before it truly signs off on an _initial_ request.
- **Multiply Your Request Power:** Make _one_ main request do the work of many! Instead of 5 new
  prompts (and 5 dings on your ~500 request counter!), use the Cursor Enhancer for 5 (or more!)
  iterative sub-prompts _within that single request's lifecycle and tool call budget_.
- **Unlock Full Tool Call Potential:** I designed this to help us guide the AI to use more of its
  ~25 available tool calls for a _single complex idea_ through those sub-prompts.
- **MCP Integration Magic:** Built on the Model Context Protocol for seamless Cursor integration.
  The popup automatically appears when needed.
- **Streamlined Linux Support:** Optimized for Linux environments with comprehensive automated
  installation and reliable performance.

## 🛠️ The Guts (How Cursor Enhancer Works)

1.  **You (or I):** Give Cursor a task (this counts as 1 main request towards your ~500).
2.  **Cursor AI:** Does its main job (coding, analysis, maybe a few tool calls from the ~25 for this
    request).
3.  **Cursor Enhancer Kicks In (The Magic Part I Evolved!):**
    - AI calls the `cursor_enhancer_chat` MCP tool automatically
    - Beautiful popup appears in Cursor with text and image input options
    - AI announces it's waiting for your input in the popup
4.  **You (in the popup):**
    - **Type** quick follow-ups (e.g., "Now add docstrings to all new functions.")
    - **Upload images** for visual context (screenshots, mockups, diagrams)
    - **Or type** `TASK_COMPLETE` when you're satisfied
5.  **Cursor AI (powered by MCP integration):** Reads your popup input (text and images), acts on it
    (more coding, _more tool calls from the original budget_!), responds in the main chat, then
    opens the popup again for your _next_ input.
6.  **Loop!** This continues, deepening the work on your original request, until you type
    `TASK_COMPLETE` in the popup.

## 🚀 Get It Going (Installation)

**Two simple steps to supercharge your Cursor workflow:**

### Step 1: One-Click Technical Setup

#### Linux Installation (Fully Tested ✅)

```bash
# Clone repository and navigate to project directory
git clone https://github.com/LakshmanTurlapati/project-cursor-enhancer.git
cd project-cursor-enhancer

# Run the magical one-click installer
./scripts/install.sh
```

The installer automatically handles:

- ✅ **Dependencies**: Package managers (apt-get), Python packages
- ✅ **MCP Server**: Global installation in `~/cursor-extensions/cursor-enhancer/`
- ✅ **Extension**: Cursor extension for the popup interface
- ✅ **Configuration**: MCP integration setup with safe merging of existing configurations

### Step 2: Copy the Rule to Cursor

**CRITICAL STEP**: For the Cursor Enhancer to work, you need to copy the rule to your Cursor
settings:

1. **Open the Rule File**: Copy the entire contents of `CursorEnhancerV2.mdc` from this folder
2. **Cursor Settings**: Open your Cursor IDE → Settings (Cmd/Ctrl + ,)
3. **Find Rules Section**: Look for "Rules" or "AI Rules" in the settings
4. **Paste & Save**: Paste the entire rule content and save
5. **Restart Cursor**: Restart Cursor completely for the rule to take effect

**Why this step?** The rule tells Cursor when and how to activate the Cursor Enhancer popup. Without
it, you'll have a working MCP server but no automatic activation!

## 🧪 Testing Your Installation

After both steps are complete:

1. **Manual Popup Test**: Press `Ctrl+Shift+R` in Cursor to open the popup manually
2. **Agent Integration Test**: Ask Cursor: _"Use the cursor_enhancer_chat tool to get my feedback"_
3. **Image Test**: Click the camera icon → upload an image → send with text
4. **Full Workflow Test**: Give Cursor a complex task and watch the Cursor Enhancer popup appear
   automatically

## 💡 Play Smart (My Tips & The "Why")

- **Why I evolved this hack:** To stop Cursor from ending too soon when I have iterative follow-ups
  for the _same original thought process_, now with the power of visual context sharing.
- **Image Context is Gold:** Upload screenshots of errors, mockups of what you want built, or
  diagrams of architecture. The AI can see and understand visual context.
- **Platform Notes:** The system is optimized for Linux environments with comprehensive automated
  installation and reliable performance.
- **Be Clear in All Inputs:** Whether typing or sharing images, clear and direct communication in
  the popup works best.
- **`TASK_COMPLETE` is Your Exit:** Don't forget to type this in the popup to let the AI finally
  rest (and free up that main request slot).

## ⚠️ Heads Up! (My Friendly Warnings)

- **EXPERIMENTAL EVOLUTION!** This is an advanced power-user tool. It works because we're very
  cleverly instructing the AI with MCP integration.
- **MCP SERVER RUNS LOCALLY:** The rule uses a local MCP server that integrates with Cursor. The
  installer sets this up automatically.
- **PLATFORM COMPATIBILITY:**
    - **Linux**: Comprehensive Ubuntu/Debian support with automated installation ✅
- **PYTHON NEEDED:** The installer handles dependencies, but your system needs to support Python 3
  for the MCP server functionality.
- **CURSOR UPDATES MIGHT CHANGE THINGS:** Future Cursor versions could affect how this rule behaves.
  What works today might need tweaks tomorrow!
- **REMEMBER THE RULE:** The MCP server is just the engine - you MUST copy the rule to your Cursor
  settings for automatic activation!

## 🎯 What You Get (Feature Summary)

### 📷 **Image Upload Power**

- Support for PNG, JPG, JPEG, GIF, BMP, WebP formats
- Drag & drop or click to upload
- Images included in MCP responses so the AI can see your visual context
- Perfect for sharing screenshots, mockups, error dialogs, or architectural diagrams

### 🎨 **Beautiful Interface**

- Clean popup with orange glow design that matches Cursor's aesthetic
- Intuitive controls for professional workflow
- Real-time MCP status indicator
- Smooth animations and responsive feedback

### 🔄 **Seamless MCP Integration**

- Works automatically with Cursor Agent tool calls
- 5-minute timeout for thoughtful responses
- Global installation works across all your Cursor projects
- File-based communication protocol for reliability

## 🔧 Troubleshooting

```bash
# Check if MCP server is running
tail -f /tmp/cursor_enhancer.log

# Check extension logs in Cursor
# Press F12 → Console tab for browser logs

# Verify MCP configuration
cat ~/.cursor/mcp.json

# Test the extension manually
# Press Ctrl+Shift+R in Cursor
```

## 🗂️ Files & Structure

```
project-cursor-enhancer/
├── cursor-extension/           # Cursor extension source
│   ├── extension.js           # Main extension file
│   ├── package.json           # Extension manifest
│   └── cursor-enhancer-3.0.0.vsix  # Built extension package
├── cursor_enhancer_mcp.py      # MCP server
├── requirements_simple.txt     # Python dependencies
├── CursorEnhancerV2.mdc       # Global rule file (COPY THIS TO CURSOR!)
├── scripts/
│   ├── install.sh             # One-click installer (Linux)
│   └── uninstall.sh          # Clean uninstaller (Linux)
├── documentation/             # Technical documentation
├── CLAUDE.md                 # Development instructions
└── README.md                 # This file
```

## 🎉 Why This Evolution?

After countless requests to evolve my original system further - **you asked for it, I delivered!**
The community response was incredible, and the demand for visual context and a more sophisticated
interface was overwhelming. This enhanced version is my answer to every feature request and
improvement suggestion focused on the core workflow enhancement.

## 🧑‍💻 About Me & This Evolution

This "Cursor Enhancer" represents the evolution of my original concept into a streamlined, visual
interaction system. It was born from my own desire to truly partner with Cursor's AI using not just
text, but visual context and iterative feedback. My goal remains the same: to make every interaction
as deep and complete as possible—and ensure every available tool call for a big idea gets its chance
to shine, making each of those ~500 requests count like gold!

The system leverages the Model Context Protocol (MCP) to create a seamless bridge between Cursor's
AI and a rich, interactive popup interface. Whether you're typing follow-ups or sharing screenshots,
it's all designed to keep you in the flow while maximizing the value of each Cursor request.

To connect with me or learn more about my work, visit:
[www.audienclature.com](https://www.audienclature.com)

---

_Happy (and supercharged) coding with Cursor! May your AI always await your final command, your
images be perfectly understood, and your monthly requests feel like they last forever!_ ✨📷
