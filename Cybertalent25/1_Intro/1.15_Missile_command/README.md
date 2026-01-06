# Missile Command

Spillet virker veldig vanskelig. Kanskje du kan jukse?

---

Lette litt kjapt gjennom spillet, men så at under Missile Command_Data/Managed/ så lå Assembly_CSharp.dll, det er ofte her spill-logikken ligger


Sjekket Assembly_CSharp.dll i DotPeek og så at når man taper havner man i scene "lose" og når man vinner havner man i scene "win"\

```csharp
  private void OnCollisionEnter2D(Collision2D collision)
  {
    if (collision.gameObject.name != "FailHitbox")
    {
      TMP_Text component = GameObject.FindGameObjectWithTag("Score").GetComponent<TMP_Text>();
      component.text = (int.Parse(component.text) + 1).ToString();
      if (((IEnumerable<GameObject>) GameObject.FindGameObjectsWithTag("Missile")).Count<GameObject>() == 1)
        SceneManager.LoadScene("Win");
      Object.Instantiate<GameObject>(this.explosionPrefab, this.transform.position, Quaternion.identity);
    }
    else
      SceneManager.LoadScene("Win"); 
    Object.Destroy((Object) this.gameObject);
  }
```
Gjorde så man havner i "win" når man taper, og tapte spillet med vilje

![Win](./Win.png)
