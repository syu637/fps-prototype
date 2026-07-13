-- Server-side hitscan example (Roblox)
-- Place as a Script under ServerScriptService. Requires a RemoteEvent named "FireWeapon" in ReplicatedStorage.
-- Simple authoritative server raycast that applies damage to Humanoids.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")

local fireEvent = ReplicatedStorage:WaitForChild("FireWeapon")

-- Utility: convert unit vector from camera pitch/yaw if client passes direction,
-- here we trust client direction minimally; for production, derive direction from player's character/attachment.

local function applyDamage(targetCharacter, damage)
    local humanoid = targetCharacter:FindFirstChildOfClass("Humanoid")
    if humanoid and humanoid.Health > 0 then
        humanoid:TakeDamage(damage)
    end
end

fireEvent.OnServerEvent:Connect(function(player, params)
    -- params: {origin = Vector3, direction = Vector3, weapon = "AR"/"SMG"/"SG"}
    if not player.Character then return end
    local origin = params.origin
    local direction = params.direction.Unit
    local weapon = params.weapon or "AR"

    if weapon == "SG" then
        -- shotgun: cast multiple pellets
        local pellets = 8
        local pelletDamage = 10
        local spreadDeg = 6 -- half-angle for near
        for i=1,pellets do
            local yaw = math.rad((math.random()-0.5) * 2 * spreadDeg)
            local pitch = math.rad((math.random()-0.5) * 2 * spreadDeg)
            -- simple rotation around axes
            local dir = CFrame.fromAxisAngle(Vector3.new(0,1,0), yaw):VectorToWorldSpace(direction)
            dir = CFrame.fromAxisAngle(Vector3.new(1,0,0), pitch):VectorToWorldSpace(dir)
            local raycastParams = RaycastParams.new()
            raycastParams.FilterDescendantsInstances = {player.Character}
            raycastParams.FilterType = Enum.RaycastFilterType.Blacklist
            local ray = Workspace:Raycast(origin, dir*1000, raycastParams)
            if ray and ray.Instance then
                local hitChar = ray.Instance:FindFirstAncestorOfClass("Model")
                if hitChar then
                    applyDamage(hitChar, pelletDamage)
                end
            end
        end
    else
        -- single hitscan
        local raycastParams = RaycastParams.new()
        raycastParams.FilterDescendantsInstances = {player.Character}
        raycastParams.FilterType = Enum.RaycastFilterType.Blacklist
        local ray = Workspace:Raycast(origin, direction*2000, raycastParams)
        if ray and ray.Instance then
            local hitChar = ray.Instance:FindFirstAncestorOfClass("Model")
            if hitChar then
                local dmg = 0
                if weapon == "AR" then dmg = 10 elseif weapon == "SMG" then dmg = 6 else dmg = 5 end
                applyDamage(hitChar, dmg)
            end
        end
    end
end)
