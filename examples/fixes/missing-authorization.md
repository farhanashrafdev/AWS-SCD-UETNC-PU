## Fix: Missing Authorization

### Before (vulnerable)

```csharp
[HttpGet("{id:int}")]
public ActionResult<UserDto> GetUser(int id)
{
    var user = users.GetById(id);
    return user is null ? NotFound() : Ok(user);
}
```

### After (fixed)

```csharp
[HttpGet("{id:int}")]
[Authorize]
public ActionResult<UserDto> GetUser(int id)
{
    var callerId = User.FindFirstValue(ClaimTypes.NameIdentifier);
    if (callerId != id.ToString())
    {
        return Forbid();
    }
    var user = users.GetById(id);
    return user is null ? NotFound() : Ok(user);
}
```

Both controls are necessary: `[Authorize]` ensures the caller is authenticated, while the ownership check ensures an authenticated user cannot read another user's record. Authentication alone is not authorization.
