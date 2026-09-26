[CmdletBinding()]
param (
    [Parameter(Position = 0)]
    [ValidateSet("setup", "run", "test", "health", "clean")]
    [string]$Command = "run"
)

$ErrorActionPreference = "Stop"

switch ($Command) {
    "setup" {
        python main.py setup
    }
    "run" {
        python main.py run
    }
    "test" {
        python main.py test
    }
    "health" {
        python main.py health
    }
    "clean" {
        python main.py clean
    }
}
