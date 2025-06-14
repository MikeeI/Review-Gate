# Installation Guide - Ubuntu/Linux

This guide provides comprehensive installation instructions for Review Gate V2 on Ubuntu and other
Debian-based Linux distributions.

## Prerequisites

### System Requirements

- **Ubuntu 20.04+ or Debian-based Linux distribution**
- **Cursor IDE** (latest version)
- **Python 3.8+** with pip and venv support
- **Audio system** (ALSA/PulseAudio) for speech-to-text functionality
- **Internet connection** for package downloads

### Verify System Requirements

```bash
# Check Ubuntu version
lsb_release -a

# Check Python version (must be 3.8+)
python3 --version

# Check if pip is available
python3 -m pip --version

# Check audio system
pulseaudio --version
# OR
cat /proc/asound/version
```

## Quick Installation (Automated)

### Option 1: One-Click Install Script

```bash
# Clone the repository
git clone https://github.com/LakshmanTurlapati/Review-Gate.git
cd Review-Gate

# Make install script executable
chmod +x scripts/install.sh

# Run the installer
./scripts/install.sh
```

The automated installer handles:

- ✅ System package updates
- ✅ SoX audio system installation
- ✅ Python virtual environment setup
- ✅ MCP server configuration
- ✅ Cursor extension preparation

## Manual Installation (Step-by-Step)

### Step 1: Install System Dependencies

```bash
# Update package lists
sudo apt update

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv sox libsox-fmt-all

# Install additional audio libraries (if needed)
sudo apt install -y pulseaudio-utils alsa-utils

# Verify installations
python3 --version
sox --version
```

### Step 2: Test Audio Recording

```bash
# Test SoX audio recording (speaks for 3 seconds)
sox -d -r 16000 -c 1 test.wav trim 0 3

# Play back the recording to verify
play test.wav

# Clean up test file
rm test.wav
```

**If audio fails:**

- Check microphone permissions
- Verify PulseAudio is running: `pulseaudio --check`
- Test with `arecord -l` to list audio devices

### Step 3: Create Installation Directory

```bash
# Create global installation directory
mkdir -p ~/cursor-extensions/review-gate-v2
cd ~/cursor-extensions/review-gate-v2

# Set proper permissions
chmod 755 ~/cursor-extensions
chmod 755 ~/cursor-extensions/review-gate-v2
```

### Step 4: Install MCP Server

```bash
# Copy MCP server files (adjust path to your clone)
cp /path/to/Review-Gate/review_gate_v2_mcp.py .
cp /path/to/Review-Gate/requirements_simple.txt .

# Create Python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements_simple.txt

# Deactivate virtual environment
deactivate
```

### Step 5: Configure MCP Integration

```bash
# Create Cursor configuration directory
mkdir -p ~/.cursor

# Create or backup existing MCP configuration
if [ -f ~/.cursor/mcp.json ]; then
    cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup.$(date +%Y%m%d_%H%M%S)
fi
```

Create the MCP configuration file:

```bash
cat > ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "review-gate-v2": {
      "command": "/home/YOUR_USERNAME/cursor-extensions/review-gate-v2/.venv/bin/python",
      "args": ["/home/YOUR_USERNAME/cursor-extensions/review-gate-v2/review_gate_v2_mcp.py"],
      "env": {
        "PYTHONPATH": "/home/YOUR_USERNAME/cursor-extensions/review-gate-v2",
        "PYTHONUNBUFFERED": "1",
        "REVIEW_GATE_MODE": "cursor_integration"
      }
    }
  }
}
EOF

# Replace YOUR_USERNAME with actual username
sed -i "s/YOUR_USERNAME/$(whoami)/g" ~/.cursor/mcp.json

# Verify JSON format
python3 -m json.tool ~/.cursor/mcp.json > /dev/null && echo "✅ MCP config is valid"
```

### Step 6: Install Cursor Extension

```bash
# Copy extension file (adjust path to your clone)
cp /path/to/Review-Gate/cursor-extension/dist/review-gate-v2-3.0.0.vsix ~/cursor-extensions/review-gate-v2/
```

**Manual Extension Installation:**

1. Open Cursor IDE
2. Press `Ctrl+Shift+P` (Linux shortcut)
3. Type "Extensions: Install from VSIX"
4. Select: `~/cursor-extensions/review-gate-v2/review-gate-v2-3.0.0.vsix`
5. Restart Cursor when prompted

### Step 7: Install Review Gate Rule

```bash
# Create Cursor rules directory (Linux path)
mkdir -p ~/.config/Cursor/User/rules

# Copy the Review Gate rule
cp /path/to/Review-Gate/ReviewGateV2.mdc ~/.config/Cursor/User/rules/

# Verify rule file
ls -la ~/.config/Cursor/User/rules/ReviewGateV2.mdc
```

## Installation Verification

### Test 1: MCP Server Test

```bash
cd ~/cursor-extensions/review-gate-v2
source .venv/bin/activate

# Run server test (should initialize without errors)
timeout 5s python review_gate_v2_mcp.py 2>&1 | grep -i "server initialized"

deactivate
```

### Test 2: Manual Popup Test

1. Open Cursor IDE
2. Press `Ctrl+Shift+R` (Linux shortcut)
3. Verify popup appears with Review Gate interface

### Test 3: Speech-to-Text Test

1. Open the Review Gate popup
2. Click the microphone icon
3. Speak clearly for 2-3 seconds
4. Click stop and verify transcription appears

### Test 4: Image Upload Test

1. Open the Review Gate popup
2. Click the camera icon
3. Select an image file (PNG, JPG, etc.)
4. Verify image appears in the interface

### Test 5: Agent Integration Test

Ask Cursor Agent: _"Use the review_gate_chat tool to get my feedback"_

## Linux-Specific Troubleshooting

### Audio Issues

**Problem: "sox: Input not found" error**

```bash
# Check audio devices
arecord -l

# Test PulseAudio
pulseaudio --check
# If failed, restart PulseAudio
pulseaudio --kill && pulseaudio --start

# Check microphone permissions
groups $USER | grep -E "audio|pulse"
# If not in audio group, add user
sudo usermod -a -G audio $USER
```

**Problem: Permission denied on audio device**

```bash
# Check audio device permissions
ls -la /dev/snd/

# Fix permissions if needed
sudo chmod 666 /dev/snd/controlC0
sudo chmod 666 /dev/snd/pcmC0D0c
```

### Python Environment Issues

**Problem: "python3-venv not found"**

```bash
# Install venv module
sudo apt install python3-venv

# Alternative: use system-wide pip
pip3 install --user -r requirements_simple.txt
```

**Problem: "No module named 'mcp'"**

```bash
# Reinstall in virtual environment
cd ~/cursor-extensions/review-gate-v2
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_simple.txt --force-reinstall
deactivate
```

### File Permission Issues

**Problem: MCP server fails to start**

```bash
# Check and fix permissions
chmod +x ~/cursor-extensions/review-gate-v2/review_gate_v2_mcp.py
chmod -R 755 ~/cursor-extensions/review-gate-v2/.venv/

# Check file ownership
ls -la ~/cursor-extensions/review-gate-v2/
# If wrong owner, fix it
sudo chown -R $USER:$USER ~/cursor-extensions/review-gate-v2/
```

### Cursor Extension Issues

**Problem: Extension not loading**

```bash
# Check Cursor configuration paths
ls -la ~/.config/Cursor/
ls -la ~/.cursor/

# Verify extension installation
find ~/.config/Cursor -name "*review-gate*" -type f
find ~/.cursor -name "*review-gate*" -type f
```

**Problem: Wrong keyboard shortcut**

- Linux uses `Ctrl+Shift+R` (not `Cmd+Shift+R`)
- Verify in Cursor: File → Preferences → Keyboard Shortcuts
- Search for "reviewGate.openChat"

### MCP Configuration Issues

**Problem: MCP server not connecting**

```bash
# Check MCP configuration
cat ~/.cursor/mcp.json

# Validate JSON format
python3 -m json.tool ~/.cursor/mcp.json

# Check server paths exist
ls -la ~/cursor-extensions/review-gate-v2/.venv/bin/python
ls -la ~/cursor-extensions/review-gate-v2/review_gate_v2_mcp.py
```

### Desktop Environment Specific

**Problem: Popup doesn't appear (Wayland)**

```bash
# Check if running Wayland
echo $XDG_SESSION_TYPE

# Some Wayland compositors may block popups
# Try switching to X11 session temporarily
```

**Problem: Audio recording fails (headless/SSH)**

```bash
# Check if audio system is available
systemctl --user status pulseaudio

# For headless systems, audio recording may not work
# Consider using text-only mode
```

## Configuration Files

### MCP Configuration Template

```json
{
    "mcpServers": {
        "review-gate-v2": {
            "command": "/home/USERNAME/cursor-extensions/review-gate-v2/.venv/bin/python",
            "args": ["/home/USERNAME/cursor-extensions/review-gate-v2/review_gate_v2_mcp.py"],
            "env": {
                "PYTHONPATH": "/home/USERNAME/cursor-extensions/review-gate-v2",
                "PYTHONUNBUFFERED": "1",
                "REVIEW_GATE_MODE": "cursor_integration"
            }
        }
    }
}
```

### Environment Variables

```bash
# Optional: Add to ~/.bashrc for persistent settings
export PYTHONPATH="$HOME/cursor-extensions/review-gate-v2"
export REVIEW_GATE_MODE="cursor_integration"
```

## Logs and Debugging

### Check MCP Server Logs

```bash
# Monitor MCP server logs
tail -f /tmp/review_gate_v2.log

# Check for errors
grep -i error /tmp/review_gate_v2.log
```

### Check Extension Logs

1. Open Cursor IDE
2. Press `F12` to open Developer Tools
3. Go to Console tab
4. Look for Review Gate related messages

### System Audio Logs

```bash
# Check PulseAudio logs
journalctl --user -u pulseaudio

# Check ALSA logs
dmesg | grep -i audio
```

## Advanced Configuration

### Custom Installation Path

```bash
# Use different installation directory
export REVIEW_GATE_DIR="$HOME/.local/share/cursor-extensions/review-gate-v2"
mkdir -p "$REVIEW_GATE_DIR"
# Update MCP configuration accordingly
```

### Service Management (Optional)

```bash
# Create systemd user service for persistent MCP server
cat > ~/.config/systemd/user/review-gate-v2.service << 'EOF'
[Unit]
Description=Review Gate V2 MCP Server
After=graphical-session.target

[Service]
Type=simple
ExecStart=/home/USERNAME/cursor-extensions/review-gate-v2/.venv/bin/python /home/USERNAME/cursor-extensions/review-gate-v2/review_gate_v2_mcp.py
Environment=PYTHONPATH=/home/USERNAME/cursor-extensions/review-gate-v2
Environment=PYTHONUNBUFFERED=1
Environment=REVIEW_GATE_MODE=cursor_integration
Restart=on-failure

[Install]
WantedBy=default.target
EOF

# Replace USERNAME and enable service
sed -i "s/USERNAME/$(whoami)/g" ~/.config/systemd/user/review-gate-v2.service
systemctl --user enable review-gate-v2.service
systemctl --user start review-gate-v2.service
```

## Uninstallation

### Complete Removal

```bash
# Stop any running services
systemctl --user stop review-gate-v2.service 2>/dev/null || true
systemctl --user disable review-gate-v2.service 2>/dev/null || true

# Remove installation directory
rm -rf ~/cursor-extensions/review-gate-v2

# Remove configuration (backup first)
cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup
# Edit ~/.cursor/mcp.json to remove review-gate-v2 entry

# Remove extension from Cursor
# Use Cursor UI: Extensions → Uninstall Review Gate V2

# Remove rule file
rm -f ~/.config/Cursor/User/rules/ReviewGateV2.mdc

# Clean up temporary files
rm -f /tmp/review_gate_*
```

## Support

### Common Issues Checklist

- [ ] Python 3.8+ installed and accessible
- [ ] Virtual environment created successfully
- [ ] SoX installed and audio recording works
- [ ] MCP configuration file is valid JSON
- [ ] Cursor extension installed and enabled
- [ ] File permissions are correct
- [ ] Keyboard shortcut is `Ctrl+Shift+R` (not Cmd)

### Getting Help

1. Check logs: `/tmp/review_gate_v2.log`
2. Verify installation: Run verification tests above
3. Check audio: Test SoX recording independently
4. Review permissions: Ensure all files are owned by your user
5. Restart Cursor: Complete restart after configuration changes

### Additional Resources

- **Main Repository**: https://github.com/LakshmanTurlapati/Review-Gate
- **Video Demo**: https://www.youtube.com/watch?v=mZmNM-AIf4M
- **Author's Site**: https://www.audienclature.com

---

_This guide focuses specifically on Ubuntu/Linux installation. For other platforms, see the main
README.md file._
