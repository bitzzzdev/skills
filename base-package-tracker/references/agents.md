# Token Optimizer - Agent Configuration Reference

This reference documents how to disable reasoning/thinking features across popular AI coding agents.

## Important Concept: API vs UI Thinking

Most agents have two distinct thinking controls:

1. **API Level (Stops Billing):** Settings that prevent the model from generating reasoning tokens in the first place
2. **UI Level (Hides Output Only):** Settings that only hide the thinking block in the UI while still billing for the tokens

**Goal of Token Optimizer:** Disable both where possible to maximize savings.

---

## OpenCode

### Configuration Paths
- Global: `~/.config/opencode/opencode.json`
- Project: `opencode.json` (current working directory)

### How to Disable

**API Level (stops reasoning tokens):**
```json
{
  "provider": {
    "cloudflare-workers-ai": {
      "models": {
        "@cf/zai-org/glm-4.7-flash": {
          "options": {
            "chat_template_kwargs": { "enable_thinking": false }
          }
        }
      }
    },
    "anthropic": {
      "models": {
        "claude-sonnet-4-5": {
          "options": { "thinking": { "type": "disabled" } }
        }
      }
    },
    "openrouter": {
      "models": {
        "deepseek/deepseek-r1:free": {
          "options": { "reasoning": { "enabled": false } }
        }
      }
    }
  }
}
```

**UI Level (hides thinking display):**
```json
{
  "$schema": "https://opencode.ai/v2/cli.json",
  "session": { "thinking": "hide" },
  "mini": { "thinking": "hide" }
}
```

### Auto-Disable Logic

The Token Optimizer:
- Parses `opencode.json` to detect existing `enable_thinking` or `thinking` values
- Sets `enable_thinking: false` if present
- Sets `thinking: "hide"` in CLI config to hide display
- Backs up original file before modifying

---

## Claude Code (Anthropic)

### Configuration Path
- Global: `~/.claude/settings.json`
- Project: `.claude/settings.local.json`

### Key Challenge

Claude Code uses **Adaptive Thinking** that can override `MAX_THINKING_TOKENS=0`. Requires disabling adaptive thinking on newer models.

### How to Disable

**Full Disable:**
```json
{
  "alwaysThinkingEnabled": false,
  "env": {
    "MAX_THINKING_TOKENS": "0",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
    "DISABLE_INTERLEAVED_THINKING": "1"
  }
}
```

**CLI Alternative:**
- Run `/config` inside Claude Code
- Disable `alwaysThinkingEnabled`
- Set `MAX_THINKING_TOKENS=0`
- Avoid prompt keywords: "think", "ultrathink", "deep think"

### Auto-Disable Logic

The Token Optimizer:
- Checks for `alwaysThinkingEnabled` in settings
- Checks for `MAX_THINKING_TOKENS` and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`
- Ensures adaptive thinking is actually disabled
- Backs up `settings.json` before modifying

---

## GitHub Copilot CLI

### Configuration Path
- Global: `~/.copilot/settings.json`

### Important: UI vs API

`Ctrl+T` only toggles UI visibility—it does NOT stop token generation.

### How to Minimize

If you must use reasoning models:

```bash
# Clamp to lowest allowed effort
copilot --effort low

# Or select a non-reasoning model
/model
```

**Recommended:** Use non-reasoning models like `gpt-4.1` or `gpt-4o` when token optimization is your priority.

### Auto-Disable Logic

The Token Optimizer:
- Creates or checks `~/.copilot/settings.json`
- Prioritizes selecting non-reasoning models over clamping effort
- Records which model is active for detection
- Backs up `settings.json`

---

## Meta Muse Code

### Configuration Path
- Global: `~/.config/muse/settings.json`

### How to Disable

Muse Code supports full on/off reasoning natively.

```json
{
  "schema_version": 1,
  "reasoning_effort": "none"
}
```

**CLI Override:**
```bash
muse --reasoning none
```

### Auto-Disable Logic

The Token Optimizer:
- Checks `reasoning_effort` in settings
- Sets to `"none"` to completely disable
- Backs up `settings.json`

---

## Google Antigravity (`agy`)

### Configuration Path
- Global: `~/.antigravity/settings.json`
- IDE settings: Antigravity Advanced Settings

### Version Differences

- **Gemini 3.x / 4.x:** Uses `thinking_level` (`MINIMAL`, `LOW`, `MEDIUM`, `HIGH`)
- **Gemini 2.5 Flash:** Uses `thinking_budget` (`0`-`1000000`)

### Full Disable (Gemini 2.5 Flash)

```json
{
  "model": {
    "modelAliasOverrides": {
      "gemini-2.5-flash": {
        "thinkingConfig": { "thinkingBudget": 0 }
      }
    }
  }
}
```

### Minimal Effort (Gemini 3.x / 4.x)

```python
from google.antigravity.types import GenerationConfig, ThinkingLevel

generation = GenerationConfig(
    thinking_level=ThinkingLevel.MINIMAL
)
```

### Auto-Disable Logic

The Token Optimizer:
- Uses `thinkingLevel: "MINIMAL"` for newer models
- Sets `thinkingBudget: 0` for Gemini 2.5 Flash
- Checks any existing `thinking_config` or `thinking_level`
- Backs up settings file

---

## OpenAI Codex CLI

### Configuration Path
- Global: `~/.codex/config.toml`
- Project: `.codex/config.toml`

### How to Disable

```toml
model = "gpt-5.4"
model_reasoning_effort = "none"
```

**CLI Override:**
```bash
codex -c 'model_reasoning_effort="none"'
```

### Model Limits

- **GPT-5.x / GPT-6.x:** Accepts `"none"` to clamp fully
- **o-series models (`o3`, `o4-mini`):** Clamp to `"low"`

### Auto-Disable Logic

The Token Optimizer:
- Sets `model_reasoning_effort = "none"` if supported
- Uses `"low"` if model requires minimum floor
- Backs up `config.toml`

---

## Google Gemini CLI

### Configuration Path
- Global: `~/.gemini/settings.json`
- Project: `.gemini/settings.json`

### UI Only vs API Only

- `ui.inlineThinkingMode: "off"` only hides UI
- `modelAliasOverrides.thinkingConfig` actually stops token generation

### How to Disable

```json
{
  "ui": {
    "inlineThinkingMode": "off"
  },
  "model": {
    "modelAliasOverrides": {
      "gemini-2.5-flash": {
        "thinkingConfig": {
          "thinkingBudget": 0
        }
      },
      "gemini-3-flash-preview": {
        "thinkingConfig": {
          "thinkingLevel": "MINIMAL"
        }
      }
    }
  }
}
```

### CLI Commands

```bash
# Settings via slash command
/settings

# Or set inlineThinkingMode manually
```

### Auto-Disable Logic

The Token Optimizer:
- Sets `inlineThinkingMode: "off"`
- Sets `thinkingBudget: 0` for 2.5 Flash
- Sets `thinkingLevel: "MINIMAL"` for 3.x / 4.x
- Backs up `settings.json`

---

## Aider

### Configuration Path
- Global: `~/.aider.conf.yml`
- Project: `.aider.conf.yml`

### Flags Used

- `thinking-tokens` (Anthropic/Gemini API budgets)
- `reasoning-effort` (OpenAI/other reasoning models)

### How to Disable

```yaml
thinking-tokens: 0
reasoning-effort: none
```

### CLI & Slash Commands

```bash
# Launch with no thinking
aider --thinking-tokens 0 --reasoning-effort none

# Inside chat
/thinking-tokens 0
/reasoning-effort none
```

### Auto-Disable Logic

The Token Optimizer:
- Sets `thinking-tokens: 0`
- Sets `reasoning-effort: none`
- Backs up `.aider.conf.yml`

---

## Cline (CLI & IDE)

### Configuration Path
- Global: `~/.cline/` (or its state directory)
- VS Code: Settings → Reasoning Effort

### How to Disable

**CLI:**
```bash
cline --thinking none
```

**VS Code / JetBrains:**
- Open settings
- Set Reasoning Effort to `None`
- Or return Thinking Budget slider to `0`

### Auto-Disable Logic

The Token Optimizer:
- Checks for `--thinking none` flag support
- Sets config to minimum if supported
- Backs up state directory

---

## Roo Code & Continue.dev

### Roo Code

- Location: Roo Code Panel → Settings (Gear Icon)
- Action: Set Reasoning Effort dropdown to `OFF` or Max Thinking Tokens to `0`

### Continue.dev

Location: `~/.continue/config.yaml`

```yaml
models:
  - name: Claude Sonnet (No Thinking)
    provider: anthropic
    model: claude-sonnet-4-5
    defaultCompletionOptions:
      reasoning: false
      reasoningBudgetTokens: 0
```

### Auto-Disable Logic

The Token Optimizer:
- Reads `config.yaml`
- Updates `defaultCompletionOptions` to disable reasoning
- Backs up config file

---

## Cursor / Windsurf

### Cursor

- Open model selector (`Ctrl+/` or `Cmd+/`)
- Choose standard model instead of *(Reasoning)* variant

### Windsurf (Cascade)

- Open Cascade model picker
- Select non-reasoning models like `GPT-4.1` or `Claude Sonnet` standard
- Avoid `(Reasoning)` or `High Effort` variants

### Auto-Disable Logic

The Token Optimizer:
- Defaults to standard model selection (no reasoning)
- Records which model variant is active
- Provides guidance if reasoning variant is detected

---

## Universal Prompt-Level Fallback

When using unsupported agents or open-weight models:

1. **Soft Switch:** Append `/no_think` to your prompt (supported natively by Qwen 3 and several fine-tunes)
2. **Router Proxy:** Route through LiteLLM/OctoAI with:
   ```yaml
   drop_params: true
   reasoning: { enabled: false }
   ```

---

## Detection Priority

When the Token Optimizer runs, it checks agents in this order:

1. Preferred agents (OpenCode, Claude Code, Aider) - modify with highest priority
2. Configurable CLI agents (Cline, Codex, Gemini, Muse)
3. IDE extension agents (Roo, Continue.dev, Cursor, Windsurf)
4. Fallback agents (Antigravity, Copilot - mostly record/recommend)

For each agent, it:
- Detects if the directory or file exists
- Reads the configuration
- Checks for existing reasoning settings
- Applies optimizations
- Creates a backup before changes
- Records what was modified in the active report

---

## Common Patterns Found

- `enable_thinking: true` → Set to `false`
- `thinking: "high"` → Set to `"hide"` or disable via API options
- `reasoning_effort: "high"` → Set to `"none"` or `"low"`
- `alwaysThinkingEnabled: true` → Set to `false` + disable adaptive thinking
- `thinkingLevel: "HIGH"` → Set to `"MINIMAL"`
- `thinkingBudget: "20000"` → Set to `"0"`

Each pattern has agent-specific overrides documented above.

---

## Restoring Original Settings

All modified files get:
```
filename.BAK
```

To restore:
```bash
# In Linux/macOS
cp ~/.config/opencode/opencode.json.BAK ~/.config/opencode/opencode.json

# In PowerShell (Windows)
Copy-Item ~/.config/opencode/opencode.json.BAK ~/.config/opencode/opencode.json
```

The Token Optimizer can restore settings if the backup exists and is newer than the current file.