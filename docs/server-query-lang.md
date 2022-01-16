# Query Lang


=> (title=~Ghoti OR priority>=4) AND deleted_at~=null
-> AND
    + (title=~Ghoti OR priority>=4)
      -> OR
        + title=~Ghoti
        + priority>=4
    + AND deleted_at~=null
== ((title.search('Ghoti')) | (priority >= 4)) & ~ (deleted_at == None)



=> (title=~Ghoti OR priority>=4) AND deleted_at~=null
-> AND { OR {title=~Ghoti, priority >=4}, deleted_at != null }
