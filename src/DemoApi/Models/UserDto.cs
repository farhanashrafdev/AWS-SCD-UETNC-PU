namespace DemoApi.Models;

/// <summary>The small, safe-to-return view of a user.</summary>
public record UserDto(int Id, string DisplayName, string Email);
